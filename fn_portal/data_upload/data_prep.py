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


def fn011(data, lake_cache, protocol_cache, user_cache):
    for item in data:
        lake = item.pop("lake")
        protocol = item.pop("protocol")
        prj_ldr = item.pop("prj_ldr", "")
        prj_cd = item.get("prj_cd")
        item["slug"] = prj_cd.lower()
        item["lake_id"] = lake_cache.get(lake)
        item["prj_ldr"] = user_cache.get(prj_ldr.upper())
        item["protocol_id"] = protocol_cache.get(protocol)
    return data


def fn022(data, fn011_cache):
    """pop off prj_cd and replace it with project_id."""
    for item in data:
        prj_cd = item.pop("prj_cd")
        ssn = item.get("ssn")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{ssn}"
        item["slug"] = slug.lower()
    return data


def fn026(data, fn011_cache):
    """pop off prj_cd and replace it with project_id."""
    for item in data:
        prj_cd = item.pop("prj_cd")
        space = item.get("space")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        slug = f"{prj_cd}-{space}"
        item["slug"] = slug.lower()
    return data


def fn028(data, fn011_cache, gear_cache):
    for item in data:
        gr = item.pop("gr")
        prj_cd = item.pop("prj_cd")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        item["gear_id"] = gear_cache.get(gr)
        slug = f"{prj_cd}-{item['mode']}"
        item["slug"] = slug.lower()
    return data


def fn121(
    data,
    fn011_cache,
    fn022_cache,
    fn026_cache,
    fn028_cache,
    grid5_cache,
    lake_abbrev="HU",
):
    # TODO - lake abbrev and grid slug....
    for item in data:
        prj_cd = item.pop("prj_cd")
        parent_key = f"{prj_cd}".lower()
        item["project_id"] = fn011_cache.get(parent_key)
        ssn = item.pop("ssn")
        space = item.pop("space")
        mode = item.pop("mode")
        grid5 = item.pop("grid5")
        grid_key = f"{lake_abbrev}-{grid5}".lower()
        sam = item["sam"]
        slug = f"{prj_cd}-{sam}".lower()
        item["slug"] = slug
        item["grid5_id"] = grid5_cache.get(grid_key)
        item["ssn_id"] = fn022_cache.get(f"{prj_cd}-{ssn}")
        item["space_id"] = fn026_cache.get(f"{prj_cd}-{space}")
        item["mode_id"] = fn028_cache.get(f"{prj_cd}-{mode}")
    return data


def fn122(data, fn121_cache):
    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.get("eff")
        fn121_key = f"{prj_cd}-{sam}".lower()
        slug = f"{prj_cd}-{sam}-{eff}".lower()
        item["sample_id"] = fn121_cache[fn121_key]
        item["slug"] = slug
    return data


def fn123(data, fn122_cache, species_cache):
    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.get("grp")
        parent_key = f"{prj_cd}-{sam}-{eff}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        item["effort_id"] = fn122_cache[parent_key]
        item["species_id"] = species_cache[spc]
        item["slug"] = slug
    return data


def fn125(data, fn123_cache):
    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.get("fish")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        item["catch_id"] = fn123_cache[parent_key]
        item["slug"] = slug
    return data


def fn125_tags(data, fn125_cache):

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
        item["fish_id"] = fn125_cache[parent_key]
        item["slug"] = slug
    return data


def fn125_lamprey(data, fn125_cache):
    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        fish_lam_id = item.get("fish_lam_id")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{fish_lam_id}".lower()
        item["fish_id"] = fn125_cache[parent_key]
        item["slug"] = slug
    return data


def fn126(data, fn125_cache):
    for item in data:
        prj_cd = item.pop("prj_cd")
        sam = item.pop("sam")
        eff = item.pop("eff")
        spc = item.pop("spc")
        grp = item.pop("grp")
        fish = item.pop("fish")
        foodid = item.get("foodid")
        parent_key = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}".lower()
        slug = f"{prj_cd}-{sam}-{eff}-{spc}-{grp}-{fish}-{foodid}".lower()
        item["fish_id"] = fn125_cache[parent_key]
        item["slug"] = slug
    return data


def fn127(data, fn125_cache):
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
        item["fish_id"] = fn125_cache[parent_key]
        item["slug"] = slug
    return data
