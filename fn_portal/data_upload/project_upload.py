"""
=============================================================
~/utils/project_upload.py
Created: Aug-12-2021 08:49
DESCRIPTION:

    connect and introspect source
    connect and introspect target

    fetch FN011
    validate FN011

    fetch FN013
    validate FN013

    fetch FN014
    validate FN014

    fetch FN022
    validate FN022

    fetch FN026
    validate FN026

    fetch FN028
    validate FN028

    fetch FN121
    validate FN121

    fetch FN122
    validate FN122

    fetch FN123
    validate FN123

    fetch FN124
    validate FN124

    fetch FN125
    validate FN125

    fetch FN125_tags
    validate FN125_tags

    fetch FN125_lamprey
    validate FN125_lamprey

    fetch FN126
    validate FN126

    fetch FN127
    validate FN127

    fetch caches for lake, species, protocol

    begin transaction
    delete old project data

    insert FN011
    insert FN013
    insert FN014
    insert FN022
    insert FN026
    insert FN028
    insert FN121
    insert FN122
    insert FN123
    insert FN124
    insert FN125
    insert FN125_tags
    insert FN125_lamprey
    insert FN126
    insert FN127

    rollback if error

    commit
    end transaction

"""

import argparse
import os

import django_settings

# from django.contrib.auth import get_user_model
from fn_portal.data_upload.fetch_utils import get_mdb_connection
from fn_portal.models import (
    FN011,
    FN022,
    FN026,
    FN028,
    FN121,
    FN122,
    FN123,
    FN125,
    FN126,
    FN127,
    FN125_Lamprey,
    FN125Tag,
)
from geoalchemy2 import Geometry
from sqlalchemy import MetaData

from data_prep import (
    prep_fn011,
    prep_fn022,
    prep_fn026,
    prep_fn028,
    prep_fn121,
    prep_fn122,
    prep_fn123,
    prep_fn125,
    prep_fn125_lamprey,
    prep_fn125_tags,
    prep_fn126,
    prep_fn127,
)
from fetch_utils import (
    execute_select,
    get_fn011_stmt,
    get_fn013_stmt,
    get_fn014_stmt,
    get_fn022_stmt,
    get_fn026_stmt,
    get_fn028_stmt,
    get_fn121_stmt,
    get_fn122_stmt,
    get_fn123_stmt,
    get_fn124_stmt,
    get_fn125_stmt,
    get_fn125lamprey_stmt,
    get_fn125tags_stmt,
    get_fn126_stmt,
    get_fn127_stmt,
)
from target_utils import (
    get_fn011_cache,
    get_fn022_cache,
    get_fn026_cache,
    get_fn028_cache,
    get_fn121_cache,
    get_fn122_cache,
    get_fn123_cache,
    get_fn125_cache,
    get_gear_cache,
    get_grid5_cache,
    get_lake_cache,
    get_protocol_cache,
    get_species_cache,
    get_trg_engine,
    get_user_attrs,
    get_user_cache,
)

SRC_DIR = "C:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/utils/data_upload_src/build/"

parser = argparse.ArgumentParser()
parser.add_argument("--src_db", "-SRC", help="Source Database")
args = parser.parse_args()

SRC_DB = args.src_db
SRC = os.path.join(SRC_DIR, SRC_DB)

src_con = get_mdb_connection(SRC)
print(f"Fetching Data from {SRC_DB}")
stmt = get_fn011_stmt()
fn011 = execute_select(src_con, stmt)
print(f"found {len(fn011)} fn011 records.")

stmt = get_fn022_stmt()
fn022 = execute_select(src_con, stmt)
print(f"found {len(fn022)} fn022 records.")

stmt = get_fn026_stmt()
fn026 = execute_select(src_con, stmt)
print(f"found {len(fn026)} fn026 records.")

stmt = get_fn028_stmt()
fn028 = execute_select(src_con, stmt)
print(f"found {len(fn028)} fn028 records.")

stmt = get_fn013_stmt()
fn013 = execute_select(src_con, stmt)
print(f"found {len(fn013)} fn013 records.")

stmt = get_fn014_stmt()
fn014 = execute_select(src_con, stmt)
print(f"found {len(fn014)} fn014 records.")

stmt = get_fn121_stmt()
fn121 = execute_select(src_con, stmt)
print(f"found {len(fn121)} fn121 records.")

stmt = get_fn122_stmt()
fn122 = execute_select(src_con, stmt)
print(f"found {len(fn122)} fn122 records.")

stmt = get_fn123_stmt()
fn123 = execute_select(src_con, stmt)
print(f"found {len(fn123)} fn123 records.")

# # stmt = get_fn124_stmt()
# # fn124 = execute_select(src_con, stmt)
# # print(f"found {len(fn124)} fn124 records.")

stmt = get_fn125_stmt()
fn125 = execute_select(src_con, stmt)
print(f"found {len(fn125)} fn125 records.")

stmt = get_fn125tags_stmt()
fn125tags = execute_select(src_con, stmt)
print(f"found {len(fn125tags)} fn125tag records.")

stmt = get_fn125lamprey_stmt()
fn125lamprey = execute_select(src_con, stmt)
print(f"found {len(fn125lamprey)} fn125lamprey records.")

stmt = get_fn126_stmt()
fn126 = execute_select(src_con, stmt)
print(f"found {len(fn126)} fn126 records.")

stmt = get_fn127_stmt()
fn127 = execute_select(src_con, stmt)
print(f"found {len(fn127)} fn127 records.")

src_con.close()

# =========================================================
# insert our data

engine = get_trg_engine()

metadata = MetaData()
metadata.reflect(bind=engine)

spc_cache = get_species_cache(engine, metadata)
lake_cache = get_lake_cache(engine, metadata)
protocol_cache = get_protocol_cache(engine, metadata)
grid5_cache = get_grid5_cache(engine, metadata)


# for each of the FN011 records we need to loop over them, pop off lake and
# protocol, and replace with their associated id's

PRJ_LDRs = list(set([x["prj_ldr"] for x in fn011]))
PRJ_CDs = list(set([x["prj_cd"] for x in fn011]))

# get or create our project leads
users = {}
for prj_ldr in PRJ_LDRs:
    users[prj_ldr] = get_user_attrs(prj_ldr)
user_cache = get_user_cache(users)


# delete our old project data:
# need to use django for now - us SA later..add()
FN011.objects.filter(prj_cd__in=PRJ_CDs).delete()

# =========================
#        FN011

data = prep_fn011(fn011, lake_cache, protocol_cache, user_cache)
items = []
for item in data:
    obj = FN011(**item)
    items.append(obj)
print("Creating FN011 records...")
FN011.objects.bulk_create(items)
fn011_cache = get_fn011_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN022

data = prep_fn022(fn022, fn011_cache)
items = []
for item in data:
    obj = FN022(**item)
    items.append(obj)
FN022.objects.bulk_create(items)
print("Creating FN022 records...")
fn022_cache = get_fn022_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN026

data = prep_fn026(fn026, fn011_cache)
items = []
for item in data:
    obj = FN026(**item)
    items.append(obj)
print("Creating FN026 records...")
FN026.objects.bulk_create(items)
fn026_cache = get_fn026_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN028

# get a gear cache
gear_cache = get_gear_cache(engine, metadata)

data = prep_fn028(fn028, fn011_cache, gear_cache)

items = []
for item in data:
    obj = FN028(**item)
    items.append(obj)
print("Creating FN028 records...")
FN028.objects.bulk_create(items)
fn028_cache = get_fn028_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN121

data = prep_fn121(
    fn121, fn011_cache, fn022_cache, fn026_cache, fn028_cache, grid5_cache
)
items = []
for item in data:
    obj = FN121(**item)
    items.append(obj)
print("Creating FN121 records...")
FN121.objects.bulk_create(items)
fn121_cache = get_fn121_cache(engine, metadata, PRJ_CDs)

# =========================
#        FN122

data = prep_fn122(fn122, fn121_cache)
items = []
for item in data:
    obj = FN122(**item)
    items.append(obj)
print("Creating FN122 records...")
FN122.objects.bulk_create(items)
fn122_cache = get_fn122_cache(engine, metadata, PRJ_CDs)

# =========================
#        FN123

data = prep_fn123(fn123, fn122_cache, spc_cache)
items = []
for item in data:
    obj = FN123(**item)
    items.append(obj)
FN123.objects.bulk_create(items)
print("Creating FN123 records...")
fn123_cache = get_fn123_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN125

data = prep_fn125(fn125, fn123_cache)
items = []
for item in data:
    obj = FN125(**item)
    items.append(obj)
print("Creating FN125 records...")
FN125.objects.bulk_create(items)
fn125_cache = get_fn125_cache(engine, metadata, PRJ_CDs)


# =========================
#        FN125-Tags

data = prep_fn125_tags(fn125tags, fn125_cache)
items = []
for item in data:
    obj = FN125Tag(**item)
    items.append(obj)
print("Creating FN125_Tag records...")
FN125Tag.objects.bulk_create(items)

# =========================
#        FN125-Lamprey

data = prep_fn125_lamprey(fn125lamprey, fn125_cache)
items = []
for item in data:
    obj = FN125_Lamprey(**item)
    items.append(obj)
print("Creating FN125_Lamprey records...")
FN125_Lamprey.objects.bulk_create(items)


# =========================
#        FN126

data = prep_fn126(fn126, fn125_cache)
items = []
for item in data:
    obj = FN126(**item)
    items.append(obj)
print("Creating FN126 records...")
FN126.objects.bulk_create(items)


# =========================
#        FN127

data = prep_fn127(fn127, fn125_cache)
items = []
for item in data:
    obj = FN127(**item)
    items.append(obj)
print("Creating FN127 records...")
FN127.objects.bulk_create(items)


print("Done!")
