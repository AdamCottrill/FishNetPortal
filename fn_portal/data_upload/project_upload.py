"""
=============================================================
~/utils/project_upload.py
Created: Aug-12-2021 08:49
DESCRIPTION:



=============================================================
"""

# import argparse

import os

import logging

from django.db import transaction, DatabaseError

from common.models import Species, Lake, Grid5

import fn_portal.models as Fnp

import fn_portal.data_upload.data_prep as prep

import fn_portal.data_upload.fetch_utils as fetch

from fn_portal.data_upload.target_utils import (
    get_id_cache,
    # get_user_attrs,
    get_user_cache,
)


logger = logging.getLogger(__name__)


def process_accdb_upload(SRC_DIR: str, SRC_DB: str):

    spc_cache = get_id_cache(Species, ["spc"])
    lake_cache = get_id_cache(Lake, ["abbrev", "lake_name"])
    protocol_cache = get_id_cache(Fnp.FNProtocol, ["abbrev"])
    grid5_cache = get_id_cache(Grid5)
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

        # check for Lakes here stop if Lenth>1

        fn011 = prep.fn011(rs, lake_cache, protocol_cache, user_cache)
        if fn011.get("errors"):
            return {"status": "error", "errors": fn011.get("errors")}
        fn011_cache = {x.slug: (i + 1) for i, x in enumerate(fn011["data"])}
        fn011_inverse = {v: k for k, v in fn011_cache.items()}

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

        logger.debug("Fetching FN028 records")
        stmt = fetch.get_fn028_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn028 = prep.fn028(rs, fn011_cache, gear_cache)
        if fn028.get("errors"):
            return {"status": "error", "errors": fn028.get("errors")}
        fn028_cache = {x.slug: (i + 1) for i, x in enumerate(fn028["data"])}
        fn028_inverse = {v: k for k, v in fn028_cache.items()}

        # stmt = fetch.get_fn013_stmt()
        # fn013 = fetch.execute_select(src_con, stmt)

        # stmt = fetch.get_fn014_stmt()
        # fn014 = fetch.execute_select(src_con, stmt)

        logger.debug("Fetching FN121 records")
        stmt = fetch.get_fn121_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn121 = prep.fn121(
            rs,
            fn011_cache,
            fn022_cache,
            fn026_cache,
            fn028_cache,
            grid5_cache,
            lake_abbrev="HU",
        )
        if fn121.get("errors"):
            return {"status": "error", "errors": fn121.get("errors")}
        fn121_cache = {x.slug: i for i, x in enumerate(fn121["data"])}
        fn121_inverse = {v: k for k, v in fn121_cache.items()}

        logger.debug("Fetching FN122 records")
        stmt = fetch.get_fn122_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn122 = prep.fn122(rs, fn121_cache)
        if fn122.get("errors"):
            return {"status": "error", "errors": fn122.get("errors")}
        fn122_cache = {x.slug: (i + 1) for i, x in enumerate(fn122["data"])}
        fn122_inverse = {v: k for k, v in fn122_cache.items()}

        logger.debug("Fetching FN123 records")
        stmt = fetch.get_fn123_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn123 = prep.fn123(rs, fn122_cache, spc_cache)
        if fn123.get("errors"):
            return {"status": "error", "errors": fn123.get("errors")}
        fn123_cache = {x.slug: (i + 1) for i, x in enumerate(fn123["data"])}
        fn123_inverse = {v: k for k, v in fn123_cache.items()}

        # # stmt = fetch.get_fn124_stmt()
        # # fn124 = fetch.execute_select(src_con, stmt)
        # # print(f"found {len(fn124)} fn124 records.")
        logger.debug("Fetching FN125 records")
        stmt = fetch.get_fn125_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn125 = prep.fn125(rs, fn123_cache)
        if fn125.get("errors"):
            return {"status": "error", "errors": fn125.get("errors")}
        fn125_cache = {x.slug: (i + 1) for i, x in enumerate(fn125["data"])}
        fn125_inverse = {v: k for k, v in fn125_cache.items()}

        logger.debug("Fetching FN125tags records")
        stmt = fetch.get_fn125tags_stmt()
        rs = fetch.execute_select(src_con, stmt)
        fn125tags = prep.fn125tags(rs, fn125_cache)
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
        fn127 = prep.fn127(rs, fn125_cache)
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
            Fnp.FN011.objects.filter(prj_cd__in=PRJ_CDs).delete()

            # =========================
            #        FN011

            # data = prep.fn011(fn011, lake_cache, protocol_cache, user_cache)
            logger.debug("Creating FN011 records...")
            items = []
            for item in fn011["data"]:
                obj = Fnp.FN011(**item.dict())
                items.append(obj)
            Fnp.FN011.objects.bulk_create(items)
            filters = {"prj_cd__in": PRJ_CDs}
            fn011_map = get_id_cache(Fnp.FN011, filters=filters)

            # =========================
            #        FN022
            logger.debug("Creating FN022 records...")
            # data = prep.fn022(fn022, fn011_cache)
            items = []
            for item in fn022["data"]:
                tmp = item.dict()
                project_id = tmp["project_id"]
                tmp["project_id"] = fn011_map[fn011_inverse[project_id]]
                obj = Fnp.FN022(**tmp)
                items.append(obj)
            Fnp.FN022.objects.bulk_create(items)
            filters = {"project__prj_cd__in": PRJ_CDs}
            fn022_map = get_id_cache(Fnp.FN022, filters=filters)

            # =========================
            #        FN026
            logger.debug("Creating FN026 records...")
            # data = prep.fn026(fn026, fn011_cache)
            items = []
            for item in fn026["data"]:
                tmp = item.dict()
                project_id = tmp["project_id"]
                tmp["project_id"] = fn011_map[fn011_inverse[project_id]]
                obj = Fnp.FN026(**tmp)
                items.append(obj)
            Fnp.FN026.objects.bulk_create(items)
            fn026_map = get_id_cache(Fnp.FN026, filters=filters)

            # =========================
            #        FN028

            # data = prep.fn028(fn028, fn011_cache, gear_cache)
            logger.debug("Creating FN028 records...")
            items = []
            for item in fn028["data"]:
                tmp = item.dict()
                project_id = tmp["project_id"]
                tmp["project_id"] = fn011_map[fn011_inverse[project_id]]
                obj = Fnp.FN028(**tmp)
                items.append(obj)
            Fnp.FN028.objects.bulk_create(items)
            fn028_map = get_id_cache(Fnp.FN028, filters=filters)

            # =========================
            #        FN121

            # our FN121 object have a save method that needs to be called - not
            # called if we bulk created them.

            # refesh_fks( for prjcd, ssn, space, mode)

            # data = prep.fn121(
            #     fn121, fn011_cache, fn022_cache, fn026_cache, fn028_cache, grid5_cache
            logger.debug("Inserting FN121 records")
            items = []
            for item in fn121["data"]:

                tmp = item.dict()
                project_id = tmp["project_id"]
                tmp["project_id"] = fn011_map[fn011_inverse[project_id]]

                ssn_id = tmp["ssn_id"]
                tmp["ssn_id"] = fn022_map[fn022_inverse[ssn_id]]

                space_id = tmp["space_id"]
                tmp["space_id"] = fn026_map[fn026_inverse[space_id]]

                mode_id = tmp["mode_id"]
                tmp["mode_id"] = fn028_map[fn028_inverse[mode_id]]

                obj = Fnp.FN121(**tmp)
                obj.save()
            fn121_map = get_id_cache(Fnp.FN121, filters=filters)

            # =========================
            #        FN122

            logger.debug("Inserting FN122 records")
            items = []
            for item in fn122["data"]:
                tmp = item.dict()
                sample_id = tmp["sample_id"]
                tmp["sample_id"] = fn121_map[fn121_inverse[sample_id]]
                obj = Fnp.FN122(**tmp)
                items.append(obj)
            Fnp.FN122.objects.bulk_create(items)
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            fn122_map = get_id_cache(Fnp.FN122, filters=filters)

            # =========================
            #        FN123

            logger.debug("Inserting FN123 records")
            items = []
            for item in fn123["data"]:
                tmp = item.dict()
                effort_id = tmp["effort_id"]
                tmp["effort_id"] = fn122_map[fn122_inverse[effort_id]]
                obj = Fnp.FN123(**tmp)
                items.append(obj)
            Fnp.FN123.objects.bulk_create(items)
            filters = {"effort__sample__project__prj_cd__in": PRJ_CDs}
            fn123_map = get_id_cache(Fnp.FN123, filters=filters)

            # =========================
            #        FN125

            logger.debug("Inserting FN125 records")
            items = []
            for item in fn125["data"]:
                tmp = item.dict()
                catch_id = tmp["catch_id"]
                tmp["catch_id"] = fn123_map[fn123_inverse[catch_id]]
                obj = Fnp.FN125(**tmp)
                items.append(obj)
            Fnp.FN125.objects.bulk_create(items)
            filters = {"catch__effort__sample__project__prj_cd__in": PRJ_CDs}
            fn125_map = get_id_cache(Fnp.FN125, filters=filters)

            # =========================
            #        FN125-Tags

            logger.debug("Inserting FN125Tags records")
            items = []
            for item in fn125tags["data"]:
                tmp = item.dict()
                fish_id = tmp["fish_id"]
                tmp["fish_id"] = fn125_map[fn125_inverse[fish_id]]
                obj = Fnp.FN125Tag(**tmp)
                items.append(obj)
            Fnp.FN125Tag.objects.bulk_create(items)

            # =========================
            #        FN125-Lamprey

            logger.debug("Inserting FN125Lamprey records")
            items = []
            for item in fn125lamprey["data"]:
                tmp = item.dict()
                fish_id = tmp["fish_id"]
                tmp["fish_id"] = fn125_map[fn125_inverse[fish_id]]
                obj = Fnp.FN125_Lamprey(**tmp)
                items.append(obj)
            Fnp.FN125_Lamprey.objects.bulk_create(items)

            # =========================
            #        FN126

            logger.debug("Inserting FN126 records")
            items = []
            for item in fn126["data"]:
                tmp = item.dict()
                fish_id = tmp["fish_id"]
                tmp["fish_id"] = fn125_map[fn125_inverse[fish_id]]
                obj = Fnp.FN126(**tmp)
                items.append(obj)
            Fnp.FN126.objects.bulk_create(items)

            # =========================
            #        FN127

            logger.debug("Inserting FN127 records")
            items = []
            for item in fn127["data"]:
                tmp = item.dict()
                fish_id = tmp["fish_id"]
                tmp["fish_id"] = fn125_map[fn125_inverse[fish_id]]
                obj = Fnp.FN127(**tmp)
                items.append(obj)
            Fnp.FN127.objects.bulk_create(items)

            return {"status": "success", "prj_cds": PRJ_CDs}

    except DatabaseError as error:
        return {"status": "insert-error", "errors": error}
