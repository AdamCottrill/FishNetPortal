"""
=============================================================
~/fn_portal/data_upload/data_prep.py
Created: Aug-12-2021 16:03
DESCRIPTION:

  Functions that take the raw data from our sql
  queries and perform final transformations before creating
  Django objects.

  TODO: consider replacing these fucntions with Pydantic Models.


A. Cottrill
=============================================================
"""

from pydantic.error_wrappers import ValidationError

from .schemas import (
    FN011,
    FN022,
    FN026,
    FN026Subspace,
    FN121,
    FN121Trawl,
    FN121Trapnet,
    FN122,
    FN122Transect,
    FN123,
    FN123NonFish,
    FN124,
    FN125Lamprey,
    FN126,
)

from .upload_utils import is_empty


def fn011(data, lake_cache, protocol_cache, user_cache):
    valid = []
    errors = []

    for item in data:
        lake = item.pop("lake")
        protocol = item.pop("protocol")
        prj_ldr = item.pop("prj_ldr", "")
        prj_cd = item.get("prj_cd")
        item["slug"] = prj_cd.lower()
        item["lake_id"] = lake_cache.get(lake)
        item["prj_ldr_id"] = user_cache.get(prj_ldr.upper())
        item["protocol_id"] = protocol_cache.get(protocol)
        try:
            tmp = FN011(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn012(data, FN012, fn011_cache, species_cache):
    """pop off prj_cd and replace it with project_id, and pop off spc and
    use it to get the species_id"""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        spc = item.pop("spc")
        grp = item.get("grp")

        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        item["species_id"] = species_cache.get(spc)
        slug = f"{prj_cd}-{spc}-{grp}"
        item["slug"] = slug.lower()
        try:
            tmp = FN012(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn022(data, fn011_cache):
    """pop off prj_cd and replace it with project_id."""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.get("ssn")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{ssn}"
        item["slug"] = slug.lower()
        try:
            tmp = FN022(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn026(data, fn011_cache):
    """pop off prj_cd and replace it with project_id."""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        space = item.get("space")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{space}"
        item["slug"] = slug.lower()
        try:
            tmp = FN026(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn026subspace(data, fn026_cache):
    """pop off prj_cd and space and replace them with space_id from the fn026_cache"""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        space = item.get("space")
        subspace = item.get("subspace")
        parent_key = f"{prj_cd}-{space}".lower()
        item["space_id"] = fn026_cache.get(parent_key)
        slug = f"{prj_cd}-{subspace}"
        item["slug"] = slug.lower()
        try:
            tmp = FN026Subspace(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn028(data, FN028, fn011_cache, gear_cache):

    valid = []
    errors = []

    for item in data:
        gr = item.pop("gr")
        prj_cd = item.pop("prj_cd")
        mode = item["mode"]
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        item["gear_id"] = gear_cache.get(gr)
        slug = f"{prj_cd}-{mode}"
        item["slug"] = slug.lower()
        try:
            tmp = FN028(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn121(
    data,
    fn011_cache,
    fn022_cache,
    fn026_subspace_cache,
    fn028_cache,
    grid5_cache,
    lake_abbrev="HU",
):
    # TODO - lake abbrev and grid slug....

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        parent_key = f"{prj_cd}".lower()
        ssn = item.pop("ssn")
        subspace = item.pop("subspace")
        mode = item.pop("mode")
        # grid5 = item.pop("grid5")
        # grid_key = f"{lake_abbrev}-{grid5}".lower()
        sam = item["sam"]
        slug = f"{prj_cd}-{sam}".lower()
        item["slug"] = slug
        item["project_id"] = fn011_cache.get(parent_key)
        # item["grid5_id"] = grid5_cache.get(grid_key)
        item["grid5_id"] = 1408  # HACK FOR TODAY!!!
        item["ssn_id"] = fn022_cache.get(f"{prj_cd}-{ssn}".lower())
        item["subspace_id"] = fn026_subspace_cache.get(f"{prj_cd}-{subspace}".lower())
        item["mode_id"] = fn028_cache.get(f"{prj_cd}-{mode}".lower())
        try:
            tmp = FN121(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn121_extension(data, schema, slug_label, fn121_cache):
    """There are several tables that are 1:1 associates with a net
    set.  These can all be handled with the same generic
    function. Just pass in a the appropriate validator."""

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-{slug_label}".lower()

        # if all(value for value in items.values()):

        if not is_empty(item):
            item["sample_id"] = fn121_cache.get(fn121_key)
            item["slug"] = slug
            try:
                tmp = schema(**item)
                valid.append(tmp)
            except ValidationError as err:
                errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn121trapnet(data, fn121_cache, bottom_type_cache, cover_type_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        bottom_type = item.pop("bottom")
        cover_type = item.pop("cover")

        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-trapnet".lower()

        if not is_empty(item):
            item["sample_id"] = fn121_cache.get(fn121_key)
            item["slug"] = slug
            item["bottom_type_id"] = bottom_type_cache.get(bottom_type)
            item["cover_type_id"] = cover_type_cache.get(cover_type)
            try:
                tmp = FN121Trapnet(**item)
                valid.append(tmp)
            except ValidationError as err:
                errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn121trawl(data, fn121_cache, vessel_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        vessel = item.pop("vessel")

        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-trapnet".lower()

        if not is_empty(item):
            item["sample_id"] = fn121_cache.get(fn121_key)
            item["slug"] = slug
            item["vessel_id"] = vessel_cache.get(vessel)

            try:
                tmp = FN121Trawl(**item)
                valid.append(tmp)
            except ValidationError as err:
                errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


# def fn121weather(data, fn121_cache):

#     valid = []
#     errors = []

#     for item in data:
#         prj_cd = item.pop("prj_cd")
#         sam = item.pop("sam")
#         fn121_key = f"{prj_cd}-{sam}".lower()
#         slug = f"{prj_cd}-{sam}-weather".lower()
#         item["sample_id"] = fn121_cache.get(fn121_key)
#         item["slug"] = slug
#         try:
#             tmp = FN121Weather(**item)
#             valid.append(tmp)
#         except ValidationError as err:
#             errors.append([item.get("slug"), err])
#     return {"data": valid, "errors": errors}


def fn122(data, fn121_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.get("eff")
        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-{eff}".lower()
        item["sample_id"] = fn121_cache.get(fn121_key)
        item["slug"] = slug
        try:
            tmp = FN122(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn122transect(data, fn121_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        track_id = item.get("track_id")
        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-{track_id}".lower()
        item["sample_id"] = fn121_cache.get(fn121_key)
        item["slug"] = slug
        try:
            tmp = FN122Transect(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn123(data, fn122_cache, species_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.get("grp")
        parent_key = f"{prj_cd}-{sam}-{eff}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        item["effort_id"] = fn122_cache.get(parent_key)
        item["species_id"] = species_cache.get(spc)
        item["slug"] = slug

        try:
            tmp = FN123(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn123nonfish(data, fn122_cache, taxon_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        taxon = item.pop("taxon")
        parent_key = f"{prj_cd}-{sam}-{eff}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{taxon}".lower()
        item["effort_id"] = fn122_cache.get(parent_key)
        item["taxon_id"] = taxon_cache.get(taxon)
        item["slug"] = slug

        try:
            tmp = FN123NonFish(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn124(data, fn123_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        siz = item.get("siz")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{siz}".lower()
        item["catch_id"] = fn123_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN124(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125(data, FN125, fn123_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.get("fish")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        item["catch_id"] = fn123_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125tags(data, FN125Tags, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        fish_tag_id = item.get("fish_tag_id")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{fish_tag_id}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125Tags(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn125lamprey(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        lamid = item.get("lamid")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{lamid}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN125Lamprey(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn126(data, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        food = item.get("food")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{food}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN126(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}


def fn127(data, FN127, fn125_cache):

    valid = []
    errors = []

    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        ageid = item.get("ageid")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{ageid}".lower()
        item["fish_id"] = fn125_cache.get(parent_key)
        item["slug"] = slug
        try:
            tmp = FN127(**item)
            valid.append(tmp)
        except ValidationError as err:
            errors.append([item.get("slug"), err])
    return {"data": valid, "errors": errors}
