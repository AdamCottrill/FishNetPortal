"""
=============================================================
~/fn_portal/data_upload/target_utils.py
Created: Aug-12-2021 12:19
DESCRIPTION:

    Utility functions to connect to our target database,
    fetch lookup caches, and insert records.

A. Cottrill
=============================================================
"""


import os

import django_settings
from django.contrib.auth import get_user_model
from sqlalchemy import MetaData, create_engine, select

User = get_user_model()


def get_user_cache(users):
    """"""
    user_cache = {}
    for key, attrs in users.items():
        if attrs:
            user, created = User.objects.get_or_create(username=attrs["username"])
            if created:
                for attr, value in attrs.items():
                    setattr(user, attr, value)
                user.save()
            user_cache[key.upper()] = user
    return user_cache


def get_user_attrs(prj_ldr):
    """take a username from a fishnet project and return the first and
    last name, a user address and an ontario email address."""
    attrs = {}
    names = prj_ldr.title().split()
    firstName = names[0]
    if len(names) > 1:
        lastName = names[1]
    else:
        lastName = ""
    attrs["first_name"] = firstName
    attrs["last_name"] = lastName
    attrs["email"] = "{}.{}@ontario.ca".format(firstName.lower(), lastName.lower())
    attrs["username"] = lastName.lower() + firstName.lower()[:2]
    return attrs


def get_trg_engine():

    PGPASSWORD = os.environ.get("PGPASSWORD")
    PGUSER = os.environ.get("PGUSER")
    DBNAME = "fn_portal"

    engine = create_engine(
        f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@localhost/{DBNAME}",
    )
    return engine


def get_species_cache(engine, metadata):

    tbl = metadata.tables["common_species"]
    stmt = select(tbl.c.id, tbl.c.spc)
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {x.spc: x.id for x in rs}
    return cache


def get_grid5_cache(engine, metadata):

    tbl = metadata.tables["common_grid5"]
    stmt = select(tbl.c.id, tbl.c.slug)
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {x.slug: x.id for x in rs}
    return cache


def get_lake_cache(engine, metadata):
    # keyed by both Lake name (Huron) and abbrev (HU)
    tbl = metadata.tables["common_lake"]
    stmt = select(tbl.c.id, tbl.c.abbrev, tbl.c.lake_name)
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        for x in rs:
            cache[x.abbrev] = x.id
            cache[x.lake_name] = x.id
    return cache


def get_protocol_cache(engine, metadata):

    tbl = metadata.tables["fn_portal_fnprotocol"]
    stmt = select(tbl.c.id, tbl.c.abbrev)
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {x.abbrev: x.id for x in rs}
    return cache


def get_gear_cache(engine, metadata):

    tbl = metadata.tables["fn_portal_gear"]
    stmt = select(tbl.c.id, tbl.c.gr_code)
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {x.gr_code: x.id for x in rs}
    return cache


def get_fn022_cache(engine, metadata, prj_cds):

    fn011 = metadata.tables["fn_portal_fn011"]
    tbl = metadata.tables["fn_portal_fn022"]
    stmt = (
        select(fn011.c.prj_cd, tbl.c.ssn, tbl.c.id)
        .join(fn011)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.ssn}": x.id for x in rs}
    return cache


def get_fn026_cache(engine, metadata, prj_cds):

    fn011 = metadata.tables["fn_portal_fn011"]
    tbl = metadata.tables["fn_portal_fn026"]
    stmt = (
        select(fn011.c.prj_cd, tbl.c.space, tbl.c.id)
        .join(fn011)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.space}": x.id for x in rs}
    return cache


def get_fn028_cache(engine, metadata, prj_cds):

    fn011 = metadata.tables["fn_portal_fn011"]
    tbl = metadata.tables["fn_portal_fn028"]
    stmt = (
        select(fn011.c.prj_cd, tbl.c.mode, tbl.c.id)
        .join(fn011)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.mode}": x.id for x in rs}
    return cache


def get_fn011_cache(engine, metadata, prj_cds):

    tbl = metadata.tables["fn_portal_fn011"]
    stmt = select(tbl.c.id, tbl.c.prj_cd).where(tbl.c.prj_cd.in_(prj_cds))
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {x.prj_cd: x.id for x in rs}
    return cache


def get_fn121_cache(engine, metadata, prj_cds):

    fn011 = metadata.tables["fn_portal_fn011"]
    tbl = metadata.tables["fn_portal_fn121"]
    stmt = (
        select(fn011.c.prj_cd, tbl.c.sam, tbl.c.id)
        .join(fn011)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.sam}": x.id for x in rs}
    return cache


def get_fn122_cache(engine, metadata, prj_cds):

    fn011 = metadata.tables["fn_portal_fn011"]
    fn121 = metadata.tables["fn_portal_fn121"]
    tbl = metadata.tables["fn_portal_fn122"]
    stmt = (
        select(fn011.c.prj_cd, fn121.c.sam, tbl.c.eff, tbl.c.id)
        .join(fn121, fn121.c.id == tbl.c.sample_id)
        .join(fn011, fn011.c.id == fn121.c.project_id)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.sam}-{x.eff}": x.id for x in rs}
    return cache


def get_fn123_cache(engine, metadata, prj_cds):

    species = metadata.tables["common_species"]
    fn011 = metadata.tables["fn_portal_fn011"]
    fn121 = metadata.tables["fn_portal_fn121"]
    fn122 = metadata.tables["fn_portal_fn122"]
    fn123 = metadata.tables["fn_portal_fn123"]

    stmt = (
        select(
            fn011.c.prj_cd,
            fn121.c.sam,
            fn122.c.eff,
            species.c.spc,
            fn123.c.grp,
            fn123.c.id,
        )
        .join(species, species.c.id == fn123.c.species_id)
        .join(fn122, fn122.c.id == fn123.c.effort_id)
        .join(fn121, fn121.c.id == fn122.c.sample_id)
        .join(fn011, fn011.c.id == fn121.c.project_id)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {f"{x.prj_cd}-{x.sam}-{x.eff}-{x.spc}-{x.grp}": x.id for x in rs}
    return cache


def get_fn125_cache(engine, metadata, prj_cds):

    species = metadata.tables["common_species"]
    fn011 = metadata.tables["fn_portal_fn011"]
    fn121 = metadata.tables["fn_portal_fn121"]
    fn122 = metadata.tables["fn_portal_fn122"]
    fn123 = metadata.tables["fn_portal_fn123"]
    fn125 = metadata.tables["fn_portal_fn125"]

    stmt = (
        select(
            fn011.c.prj_cd,
            fn121.c.sam,
            fn122.c.eff,
            species.c.spc,
            fn123.c.grp,
            fn125.c.fish,
            fn125.c.id,
        )
        .join(fn123, fn123.c.id == fn125.c.catch_id)
        .join(species, species.c.id == fn123.c.species_id)
        .join(fn122, fn122.c.id == fn123.c.effort_id)
        .join(fn121, fn121.c.id == fn122.c.sample_id)
        .join(fn011, fn011.c.id == fn121.c.project_id)
        .where(fn011.c.prj_cd.in_(prj_cds))
    )
    cache = {}
    with engine.connect() as conn:
        rs = conn.execute(stmt)
        cache = {
            f"{x.prj_cd}-{x.sam}-{x.eff}-{x.spc}-{x.grp}-{x.fish}": x.id for x in rs
        }
    return cache
