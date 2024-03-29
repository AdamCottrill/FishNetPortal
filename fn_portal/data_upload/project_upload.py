"""
=============================================================
~/utils/project_upload.py
Created: Aug-12-2021 08:49
DESCRIPTION:



=============================================================
"""

# import argparse


import logging
import os

import fn_portal.data_upload.data_prep as prep
import fn_portal.data_upload.fetch_utils as fetch
import fn_portal.models as Fnp
from common.models import BottomType, CoverType, Grid5, Lake, Species, Taxon, Vessel
from django.db import DatabaseError, transaction
from django.db.models import Count, OuterRef, Subquery

# todo - replace these with dynamic queries from common:
from .choices import (
    ageprep1_choices,
    ageprep2_choices,
    agest_choices,
    clip_choices,
    gruse_choices,
    orient_choices,
    tag_agency_choices,
    tag_colour_choices,
    tag_position_choices,
    tag_type_choices,
    tissue_choices,
    waveform_choices,
)
from .schemas import (
    FN012Factory,
    FN028Factory,
    FN121ElectroFishingFactory,
    FN121Limno,
    FN121Weather,
    FN125Factory,
    FN125TagsFactory,
    FN127Factory,
)
from .target_utils import get_id_cache, get_user_cache
from .upload_utils import (
    batch_update_model,
    create_update_delete,
    get_create_update_delete,
    int_or_none,
    parse_compound_field,
    parse_wind,
)

logger = logging.getLogger(__name__)


def process_accdb_upload(SRC_DIR: str, SRC_DB: str):

    spc_cache = get_id_cache(Species, ["spc"])
    taxon_cache = get_id_cache(Taxon, ["itiscode"])

    lake_cache = get_id_cache(Lake, ["abbrev", "lake_name"])
    protocol_cache = get_id_cache(Fnp.FNProtocol, ["abbrev"])

    gear_cache = get_id_cache(Fnp.Gear, ["gr_code"])
    user_cache = get_user_cache()

    # for each of the FN011 records we need to loop over them, pop off lake and
    # protocol, and replace with their associated id's

    SRC = os.path.join(SRC_DIR, SRC_DB)

    src_con = fetch.get_mdb_connection(SRC)
    try:

        logger.debug("Fetching FN011 records")
        stmt = fetch.get_fn011_stmt()
        rs = fetch.execute_select(src_con, stmt)

        PRJ_CDs = list(set([x["prj_cd"] for x in rs]))
        LAKES = list(set([x["lake"] for x in rs]))
        LAKES.sort()

        # verify that only one lake is included in our LAKES array:

        if len(LAKES) == 1 or LAKES == ["ER", "SC"]:
            # get the grids for our lake:
            grid5_cache = get_id_cache(Grid5, filters={"lake__abbrev__in": LAKES})
        else:
            msg = (
                "Lake was missing or multiple lakes were found. Lake is required "
                + "must be *one* of 'SU', 'HU', 'ON', 'ER', 'SC'"
                + " or ['SC', 'ER']. Please split the upload by lake and try again."
            )
            return {"status": "insert-error", "errors": msg}

        # check for Lakes here stop if Lenth>1

        fn011 = prep.fn011(rs, lake_cache, protocol_cache, user_cache)
        if fn011.get("errors"):
            return {"status": "error", "errors": fn011.get("errors")}
        fn011_cache = {x.slug: (i + 1) for i, x in enumerate(fn011["data"])}
        fn011_inverse = {v: k for k, v in fn011_cache.items()}

        logger.debug("Fetching FN012 records")
        stmt = fetch.get_fn012_stmt()
        rs = fetch.execute_select(src_con, stmt)
        FN011_validator = FN012Factory(agest_choices=agest_choices)
        fn012 = prep.fn012(rs, FN011_validator, fn011_cache, spc_cache)
        if fn012.get("errors"):
            return {"status": "error", "errors": fn012.get("errors")}

        logger.debug("Fetching FN022 records")
        stmt = fetch.get_fn022_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn022 = prep.fn022(rs, fn011_cache)
        if fn022.get("errors"):
            return {"status": "error", "errors": fn022.get("errors")}
        fn022_cache = {x.slug: (i + 1) for i, x in enumerate(fn022["data"])}
        fn022_inverse = {v: k for k, v in fn022_cache.items()}

        logger.debug("Fetching FN026 records")
        stmt = fetch.get_fn026_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn026 = prep.fn026(rs, fn011_cache)
        if fn026.get("errors"):
            return {"status": "error", "errors": fn026.get("errors")}
        fn026_cache = {x.slug: (i + 1) for i, x in enumerate(fn026["data"])}
        fn026_inverse = {v: k for k, v in fn026_cache.items()}

        logger.debug("Fetching FN026Subspace records")
        stmt = fetch.get_fn026_subspace_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn026subspace = prep.fn026subspace(rs, fn026_cache)
        if fn026subspace.get("errors"):
            return {"status": "error", "errors": fn026subspace.get("errors")}
        fn026_subspace_cache = {
            x.slug: (i + 1) for i, x in enumerate(fn026subspace["data"])
        }
        fn026subspace_inverse = {v: k for k, v in fn026_subspace_cache.items()}

        logger.debug("Fetching FN028 records")
        stmt = fetch.get_fn028_stmt()
        rs = fetch.execute_select(src_con, stmt)
        FN028_validator = FN028Factory(
            orient_choices=orient_choices, gruse_choices=gruse_choices
        )
        fn028 = prep.fn028(rs, FN028_validator, fn011_cache, gear_cache)
        if fn028.get("errors"):
            return {"status": "error", "errors": fn028.get("errors")}
        fn028_cache = {x.slug: (i + 1) for i, x in enumerate(fn028["data"])}
        fn028_inverse = {v: k for k, v in fn028_cache.items()}

        # this assumes that Lake St. grids start with ER:

        logger.debug("Fetching FN121 records")
        stmt = fetch.get_fn121_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121 = prep.fn121(
            rs,
            fn011_cache,
            fn022_cache,
            fn026_subspace_cache,
            fn028_cache,
            grid5_cache,
            lake_abbrev=LAKES[0],
        )
        if fn121.get("errors"):
            return {"status": "error", "errors": fn121.get("errors")}
        fn121_cache = {x.slug: i for i, x in enumerate(fn121["data"])}
        fn121_inverse = {v: k for k, v in fn121_cache.items()}

        logger.debug("Fetching FN121LIMNO records")
        stmt = fetch.get_fn121limno_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121limno = prep.fn121_extension(rs, FN121Limno, "limno", fn121_cache)
        # fn121limno = prep.fn121limno(rs, fn121_cache)
        if fn121limno.get("errors"):
            return {"status": "error", "errors": fn121limno.get("errors")}

        logger.debug("Fetching FN121TRAWL records")
        vessel_cache = get_id_cache(Vessel, ["abbrev"])
        stmt = fetch.get_fn121trawl_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121trawl = prep.fn121trawl(rs, fn121_cache, vessel_cache)
        # fn121trawl = prep.fn121trawl(rs, fn121_cache)
        if fn121trawl.get("errors"):
            return {"status": "error", "errors": fn121trawl.get("errors")}

        logger.debug("Fetching FN121TRAPNET records")

        bottom_type_cache = get_id_cache(BottomType, ["abbrev"])
        cover_type_cache = get_id_cache(CoverType, ["abbrev"])

        stmt = fetch.get_fn121trapnet_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121trapnet = prep.fn121trapnet(
            rs, fn121_cache, bottom_type_cache, cover_type_cache
        )
        # fn121trapnet = prep.fn121trapnet(rs, fn121_cache)
        if fn121trapnet.get("errors"):
            return {"status": "error", "errors": fn121trapnet.get("errors")}

        logger.debug("Fetching FN121WEATHER records")
        stmt = fetch.get_fn121weather_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121weather = prep.fn121_extension(rs, FN121Weather, "weather", fn121_cache)
        if fn121weather.get("errors"):
            return {"status": "error", "errors": fn121weather.get("errors")}

        logger.debug("Fetching FN121ELECTROFISHING records")

        stmt = fetch.get_fn121electrofishing_stmt()
        rs = fetch.execute_select(src_con, stmt)
        FN121EFishing_validator = FN121ElectroFishingFactory(
            waveform_choices=waveform_choices
        )
        fn121electrofishing = prep.fn121electrofishing(
            rs,
            FN121EFishing_validator,
            fn121_cache,
        )
        if fn121electrofishing.get("errors"):
            return {"status": "error", "errors": fn121electrofishing.get("errors")}

        logger.debug("Fetching FN122 records")
        stmt = fetch.get_fn122_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn122 = prep.fn122(rs, fn121_cache)
        if fn122.get("errors"):
            return {"status": "error", "errors": fn122.get("errors")}
        fn122_cache = {x.slug: (i + 1) for i, x in enumerate(fn122["data"])}
        fn122_inverse = {v: k for k, v in fn122_cache.items()}

        # TO DO: trasect data here
        logger.debug("Fetching FN121 GPS Track records")
        stmt = fetch.get_fn121gpstrack_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121gpstrack = prep.fn121gpstrack(rs, fn121_cache)
        if fn121gpstrack.get("errors"):
            return {"status": "error", "errors": fn121gpstrack.get("errors")}

        logger.debug("Fetching FN123 records")
        stmt = fetch.get_fn123_stmt()
        rs = fetch.execute_select(src_con, stmt)
        # TODO: - replace spc_cache with FN012 cache
        fn123 = prep.fn123(rs, fn122_cache, spc_cache)
        if fn123.get("errors"):
            return {"status": "error", "errors": fn123.get("errors")}
        fn123_cache = {x.slug: (i + 1) for i, x in enumerate(fn123["data"])}
        fn123_inverse = {v: k for k, v in fn123_cache.items()}

        logger.debug("Fetching FN123nonfish records")
        stmt = fetch.get_fn123nonfish_stmt()
        rs = fetch.execute_select(src_con, stmt)
        # TODO: - replace spc_cache with FN012 cache
        fn123nonfish = prep.fn123nonfish(rs, fn122_cache, taxon_cache)
        if fn123nonfish.get("errors"):
            return {"status": "error", "errors": fn123nonfish.get("errors")}

        logger.debug("Fetching FN124 records")
        stmt = fetch.get_fn124_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn124 = prep.fn124(rs, fn123_cache)
        if fn124.get("errors"):
            return {"status": "error", "errors": fn124.get("errors")}

        logger.debug("Fetching FN125 records")
        stmt = fetch.get_fn125_stmt()
        rs = fetch.execute_select(src_con, stmt)
        FN125_validator = FN125Factory(
            tissue_choices=tissue_choices, clip_choices=clip_choices
        )
        fn125 = prep.fn125(rs, FN125_validator, fn123_cache)
        if fn125.get("errors"):
            return {"status": "error", "errors": fn125.get("errors")}
        fn125_cache = {x.slug: (i + 1) for i, x in enumerate(fn125["data"])}
        fn125_inverse = {v: k for k, v in fn125_cache.items()}

        logger.debug("Fetching FN125tags records")
        stmt = fetch.get_fn125tags_stmt()
        rs = fetch.execute_select(src_con, stmt)

        FN125Tags_validator = FN125TagsFactory(
            tag_type_choices=tag_type_choices,
            tag_position_choices=tag_position_choices,
            tag_agency_choices=tag_agency_choices,
            tag_colour_choices=tag_colour_choices,
        )

        fn125tags = prep.fn125tags(rs, FN125Tags_validator, fn125_cache)
        if fn125tags.get("errors"):
            return {"status": "error", "errors": fn125tags.get("errors")}

        logger.debug("Fetching FN125Lamprey records")
        stmt = fetch.get_fn125lamprey_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn125lamprey = prep.fn125lamprey(rs, fn125_cache)
        if fn125lamprey.get("errors"):
            return {"status": "error", "errors": fn125lamprey.get("errors")}

        logger.debug("Fetching FN126 records")
        stmt = fetch.get_fn126_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn126 = prep.fn126(rs, fn125_cache)
        if fn126.get("errors"):
            return {"status": "error", "errors": fn126.get("errors")}

        logger.debug("Fetching FN127 records")
        stmt = fetch.get_fn127_stmt()
        rs = fetch.execute_select(src_con, stmt)
        FN127_validator = FN127Factory(
            agest_choices=agest_choices,
            ageprep1_choices=ageprep1_choices,
            ageprep2_choices=ageprep2_choices,
        )
        fn127 = prep.fn127(rs, FN127_validator, fn125_cache)
        if fn127.get("errors"):
            return {"status": "error", "errors": fn127.get("errors")}

    finally:
        src_con.close()

    # if there are any error stop and report them here...

    # =========================================================
    # insert our data

    try:
        with transaction.atomic():

            # delete our old project data:
            # need to use django for now - us SA later..add()
            # Fnp.FN011.objects.filter(prj_cd__in=PRJ_CDs).delete()

            # =========================
            #        FN011

            # data = prep.fn011(fn011, lake_cache, protocol_cache, user_cache)
            logger.debug("Creating FN011 records...")
            for item in fn011["data"]:
                obj, created = Fnp.FN011.objects.update_or_create(
                    prj_cd=item.prj_cd, defaults=item.dict()
                )
                obj.status = "validated"
                obj.save()
            filters = {"prj_cd__in": PRJ_CDs}
            fn011_map = get_id_cache(Fnp.FN011, filters=filters)

            # =========================
            #        FN012
            logger.debug("Creating FN012 records...")

            data = [x.dict() for x in fn012["data"]]

            filters = {"project__prj_cd__in": PRJ_CDs}
            create_slugs, update_slugs, delete_slugs = get_create_update_delete(
                Fnp.FN012, filters, data
            )

            Fnp.FN012.objects.filter(slug__in=delete_slugs).delete()

            to_be_created = []
            updates = {}

            for item in [x for x in data if x["slug"] in create_slugs + update_slugs]:

                spcmrk = item.pop("spcmrk")
                item["spcmrk1"] = spcmrk[0]
                item["spcmrk2"] = None if len(spcmrk) == 1 else spcmrk[1]

                fdsam = item.pop("fdsam")
                item["fdsam1"] = fdsam[0]
                item["fdsam2"] = None if len(fdsam) == 1 else fdsam[1]

                project_id = item["project_id"]
                item["project_id"] = fn011_map[fn011_inverse[project_id]]

                if item["slug"] in create_slugs:
                    to_be_created.append(Fnp.FN012(**item))
                else:
                    updates[item["slug"]] = item

            Fnp.FN012.objects.bulk_create(to_be_created)
            batch_update_model(Fnp.FN012, update_slugs, updates)

            # =========================
            #        FN022
            logger.debug("Creating FN022 records...")

            data = [x.dict() for x in fn022["data"]]
            create_update_delete(
                data, Fnp.FN022, filters, "project_id", fn011_map, fn011_inverse
            )
            fn022_map = get_id_cache(Fnp.FN022, filters=filters)

            # =========================
            #        FN026
            logger.debug("Creating FN026 records...")
            # data = prep.fn026(fn026, fn011_cache)

            data = [x.dict() for x in fn026["data"]]
            create_update_delete(
                data, Fnp.FN026, filters, "project_id", fn011_map, fn011_inverse
            )
            fn026_map = get_id_cache(Fnp.FN026, filters=filters)

            # =========================
            #        FN026subspace
            logger.debug("Creating FN026subspace records...")
            subspace_filters = {"space__project__prj_cd__in": PRJ_CDs}
            data = [x.dict() for x in fn026subspace["data"]]
            create_update_delete(
                data,
                Fnp.FN026Subspace,
                subspace_filters,
                "space_id",
                fn026_map,
                fn026_inverse,
            )
            fn026subspace_map = get_id_cache(
                Fnp.FN026Subspace, filters=subspace_filters
            )

            # =========================
            #        FN028

            # data = prep.fn028(fn028, fn011_cache, gear_cache)
            logger.debug("Creating FN028 records...")
            data = [x.dict() for x in fn028["data"]]
            create_update_delete(
                data, Fnp.FN028, filters, "project_id", fn011_map, fn011_inverse
            )
            fn028_map = get_id_cache(Fnp.FN028, filters=filters)

            # =========================
            #        FN121

            # our FN121 object have a save method that needs to be called - it is not
            # called if we bulk created them.

            # refesh_fks( for prjcd, ssn, space, mode)

            # data = prep.fn121(
            #     fn121, fn011_cache, fn022_cache, fn026_cache, fn028_cache, grid5_cache)

            logger.debug("Inserting and Updating FN121 records")

            data = [x.dict() for x in fn121["data"]]
            create_slugs, update_slugs, delete_slugs = get_create_update_delete(
                Fnp.FN121, filters, data
            )
            Fnp.FN121.objects.filter(slug__in=delete_slugs).delete()
            to_be_created = []
            updates = {}

            for item in [x for x in data if x["slug"] in create_slugs + update_slugs]:
                # call preprocessor here to make any necessary transformation to each item
                # what needs to be done depends on the current model.

                project_id = item["project_id"]
                item["project_id"] = fn011_map[fn011_inverse[project_id]]

                ssn_id = item["ssn_id"]
                item["ssn_id"] = fn022_map[fn022_inverse[ssn_id]]

                subspace_id = item["subspace_id"]
                item["subspace_id"] = fn026subspace_map[
                    fn026subspace_inverse[subspace_id]
                ]

                mode_id = item["mode_id"]
                item["mode_id"] = fn028_map[fn028_inverse[mode_id]]

                if item["slug"] in create_slugs:
                    obj = Fnp.FN121(**item)
                    obj.save()
                else:
                    # update item:
                    obj = Fnp.FN121.objects.get(slug=item["slug"])
                    for attr in item:
                        if getattr(obj, attr) != item[attr]:
                            setattr(obj, attr, item[attr])
                    obj.save()

            fn121_map = get_id_cache(Fnp.FN121, filters=filters)

            # =========================
            #        FN121Limno

            logger.debug("Inserting and Updating FN121Limno records")

            data = [x.dict() for x in fn121limno["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            create_update_delete(
                data, Fnp.FN121Limno, filters, "sample_id", fn121_map, fn121_inverse
            )

            # =========================
            #        FN121Trapnet

            logger.debug("Inserting and Updating FN121Trapnet records")

            data = [x.dict() for x in fn121trapnet["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            create_update_delete(
                data, Fnp.FN121Trapnet, filters, "sample_id", fn121_map, fn121_inverse
            )

            # =========================
            #        FN121Trawl

            logger.debug("Inserting and Updating FN121Trawl records")

            data = [x.dict() for x in fn121trawl["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            create_update_delete(
                data, Fnp.FN121Trawl, filters, "sample_id", fn121_map, fn121_inverse
            )

            # =========================
            #        FN121Weather

            logger.debug("Inserting and Updating FN121Weather records")

            data = [x.dict() for x in fn121weather["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}

            create_slugs, update_slugs, delete_slugs = get_create_update_delete(
                Fnp.FN121Weather, filters, data
            )

            Fnp.FN121Weather.objects.filter(slug__in=delete_slugs).delete()

            to_be_created = []
            updates = {}

            for item in [x for x in data if x["slug"] in create_slugs + update_slugs]:
                wind = item.pop("wind0")
                wind_direction, wind_speed = parse_wind(wind)
                item["wind_direction0"] = wind_direction
                item["wind_speed0"] = wind_speed

                wind = item.pop("wind1")
                wind_direction, wind_speed = parse_wind(wind)
                item["wind_direction1"] = wind_direction
                item["wind_speed1"] = wind_speed

                xweather = item.pop("xweather")
                precip_duration, wave_duration = parse_compound_field(xweather)

                item["precip_duration"] = int_or_none(precip_duration)
                item["wave_duration"] = int_or_none(wave_duration)

                sample_id = item["sample_id"]
                item["sample_id"] = fn121_map[fn121_inverse[sample_id]]

                if item["slug"] in create_slugs:
                    to_be_created.append(Fnp.FN121Weather(**item))
                else:
                    updates[item["slug"]] = item

            Fnp.FN121Weather.objects.bulk_create(to_be_created)
            batch_update_model(Fnp.FN121Weather, update_slugs, updates)

            # =========================
            #        FN121Electrofishing

            logger.debug("Inserting and Updating FN121Electrofishing records")

            data = [x.dict() for x in fn121electrofishing["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            create_update_delete(
                data,
                Fnp.FN121ElectroFishing,
                filters,
                "sample_id",
                fn121_map,
                fn121_inverse,
            )

            # =========================
            #        FN122

            logger.debug("Inserting and Updating FN122 records")

            data = [x.dict() for x in fn122["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}

            create_update_delete(
                data, Fnp.FN122, filters, "sample_id", fn121_map, fn121_inverse
            )

            fn122_map = get_id_cache(Fnp.FN122, filters=filters)

            # =========================
            #        FN121GpsTrack

            logger.debug("Inserting and Updating FN121GpsTrack records")

            data = [x.dict() for x in fn121gpstrack["data"]]
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            create_update_delete(
                data, Fnp.FN121GpsTrack, filters, "sample_id", fn121_map, fn121_inverse
            )
            # no inverse map for fn121gpstrack because it has no children

            # =========================
            #        FN123

            logger.debug("Inserting and Updating FN123 records")
            filters = {"effort__sample__project__prj_cd__in": PRJ_CDs}
            data = [x.dict() for x in fn123["data"]]
            create_update_delete(
                data, Fnp.FN123, filters, "effort_id", fn122_map, fn122_inverse
            )

            fn123_map = get_id_cache(Fnp.FN123, filters=filters)

            # =========================
            #        FN123 Non Fish

            logger.debug("Inserting and Updating FN123 Non-Fish records")
            filters = {"effort__sample__project__prj_cd__in": PRJ_CDs}
            data = [x.dict() for x in fn123nonfish["data"]]
            create_update_delete(
                data, Fnp.FN123NonFish, filters, "effort_id", fn122_map, fn122_inverse
            )

            # =========================
            #        FN124

            logger.debug("Inserting and Updating FN124 records")
            filters = {"catch__effort__sample__project__prj_cd__in": PRJ_CDs}
            data = [x.dict() for x in fn124["data"]]
            create_update_delete(
                data, Fnp.FN124, filters, "catch_id", fn123_map, fn123_inverse
            )

            # =========================
            #        FN125

            logger.debug("Inserting and Updating FN125 records")

            data = [x.dict() for x in fn125["data"]]
            create_update_delete(
                data, Fnp.FN125, filters, "catch_id", fn123_map, fn123_inverse
            )

            fn125_map = get_id_cache(Fnp.FN125, filters=filters)

            # Update FN123.biocnt once all of our FN125 objects have been created
            # using update and a subquery
            biocnts = (
                Fnp.FN125.objects.filter(catch=OuterRef("pk"))
                .order_by()
                .values("catch_id")
                .annotate(biocnt=Count("*"))
                .values("biocnt")
            )
            Fnp.FN123.objects.filter(
                effort__sample__project__prj_cd__in=PRJ_CDs
            ).update(biocnt=Subquery(biocnts))

            # =========================
            #        FN125-Tags

            logger.debug("Inserting and Updating FN125Tags records")
            filters = {"fish__catch__effort__sample__project__prj_cd__in": PRJ_CDs}
            data = [x.dict() for x in fn125tags["data"]]
            create_update_delete(
                data, Fnp.FN125Tag, filters, "fish_id", fn125_map, fn125_inverse
            )

            # =========================
            #        FN125-Lamprey

            logger.debug("Inserting and Updating FN125Lamprey records")
            data = [x.dict() for x in fn125lamprey["data"]]
            create_update_delete(
                data, Fnp.FN125_Lamprey, filters, "fish_id", fn125_map, fn125_inverse
            )

            # =========================
            #        FN126

            logger.debug("Inserting and Updating FN126 records")
            data = [x.dict() for x in fn126["data"]]
            create_update_delete(
                data, Fnp.FN126, filters, "fish_id", fn125_map, fn125_inverse
            )

            # =========================
            #        FN127

            logger.debug("Inserting and Updating FN127 records")
            data = [x.dict() for x in fn127["data"]]
            create_update_delete(
                data, Fnp.FN127, filters, "fish_id", fn125_map, fn125_inverse
            )

            return {"status": "success", "prj_cds": PRJ_CDs}

    except DatabaseError as error:
        return {"status": "insert-error", "errors": error}
