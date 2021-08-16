"""
=============================================================
~/utils/project_upload.py
Created: Aug-12-2021 08:49
DESCRIPTION:



=============================================================
"""

#import argparse

import os
from typing import List, Union

from django.db import transaction, DatabaseError

#import django_settings

from common.models import Species, Lake, Grid5

import fn_portal.models as Fnp

import fn_portal.data_upload.data_prep  as prep

import fn_portal.data_upload.fetch_utils as fetch

from fn_portal.data_upload.target_utils import (
    get_id_cache,
    get_user_attrs,
    get_user_cache,
)


## SRC_DIR = "C:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/utils/data_upload_src/build/"
##
## parser = argparse.ArgumentParser()
## parser.add_argument("--src_db", "-SRC", help="Source Database")
## args = parser.parse_args()
##
## SRC_DB = args.src_db
##

def process_accdb_upload(SRC_DIR:str, SRC_DB:str) -> Union[List, str]:

    SRC = os.path.join(SRC_DIR, SRC_DB)

    src_con = fetch.get_mdb_connection(SRC)

    stmt = fetch.get_fn011_stmt()
    fn011 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn022_stmt()
    fn022 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn026_stmt()
    fn026 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn028_stmt()
    fn028 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn013_stmt()
    fn013 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn014_stmt()
    fn014 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn121_stmt()
    fn121 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn122_stmt()
    fn122 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn123_stmt()
    fn123 = fetch.execute_select(src_con, stmt)

    # # stmt = fetch.get_fn124_stmt()
    # # fn124 = fetch.execute_select(src_con, stmt)
    # # print(f"found {len(fn124)} fn124 records.")

    stmt = fetch.get_fn125_stmt()
    fn125 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn125tags_stmt()
    fn125tags = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn125lamprey_stmt()
    fn125lamprey = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn126_stmt()
    fn126 = fetch.execute_select(src_con, stmt)

    stmt = fetch.get_fn127_stmt()
    fn127 = fetch.execute_select(src_con, stmt)

    src_con.close()


    #if there are any error stop and report them here...

    # =========================================================
    # insert our data

    spc_cache = get_id_cache(Species, ["spc"])
    lake_cache = get_id_cache(Lake, ["abbrev", "lake_name"])
    protocol_cache = get_id_cache(Fnp.FNProtocol, ["abbrev"])
    grid5_cache = get_id_cache(Grid5)


    # for each of the FN011 records we need to loop over them, pop off lake and
    # protocol, and replace with their associated id's

    PRJ_LDRs = list(set([x["prj_ldr"] for x in fn011]))
    PRJ_CDs = list(set([x["prj_cd"] for x in fn011]))

    # get or create our project leads
    users = {}
    for prj_ldr in PRJ_LDRs:
        users[prj_ldr] = get_user_attrs(prj_ldr)
    user_cache = get_user_cache(users)

    try:
        with transaction.atomic():

            # delete our old project data:
            # need to use django for now - us SA later..add()
            Fnp.FN011.objects.filter(prj_cd__in=PRJ_CDs).delete()

            # =========================
            #        FN011

            data = prep.fn011(fn011, lake_cache, protocol_cache, user_cache)
            items = []
            for item in data:
                obj = Fnp.FN011(**item)
                items.append(obj)
            Fnp.FN011.objects.bulk_create(items)
            filters = {"prj_cd__in": PRJ_CDs}
            fn011_cache = get_id_cache(Fnp.FN011, filters=filters)

            # =========================
            #        FN022

            data = prep.fn022(fn022, fn011_cache)
            items = []
            for item in data:
                obj = Fnp.FN022(**item)
                items.append(obj)
            Fnp.FN022.objects.bulk_create(items)
            filters = {"project__prj_cd__in": PRJ_CDs}
            fn022_cache = get_id_cache(Fnp.FN022, filters=filters)


            # =========================
            #        FN026

            data = prep.fn026(fn026, fn011_cache)
            items = []
            for item in data:
                obj = Fnp.FN026(**item)
                items.append(obj)
            Fnp.FN026.objects.bulk_create(items)
            fn026_cache = get_id_cache(Fnp.FN026, filters=filters)

            # =========================
            #        FN028

            # get a gear cache
            gear_cache = get_id_cache(Fnp.
                Gear,
                [
                    "gr_code",
                ],
            )


            data = prep.fn028(fn028, fn011_cache, gear_cache)

            items = []
            for item in data:
                obj = Fnp.FN028(**item)
                items.append(obj)
            Fnp.FN028.objects.bulk_create(items)
            fn028_cache = get_id_cache(Fnp.FN028, filters=filters)

            # =========================
            #        FN121

            # our FN121 object have a save method that needs to be called - not
            # called if we bulk created them.

            print("Creating FN121 records...")
            data = prep.fn121(
                fn121, fn011_cache, fn022_cache, fn026_cache, fn028_cache, grid5_cache
            )
            items = []
            for item in data:
                obj = Fnp.FN121(**item)
                obj.save()
            fn121_cache = get_id_cache(Fnp.FN121, filters=filters)


            # =========================
            #        FN122

            data = prep.fn122(fn122, fn121_cache)
            items = []
            for item in data:
                obj = Fnp.FN122(**item)
                items.append(obj)
            Fnp.FN122.objects.bulk_create(items)
            filters = {"sample__project__prj_cd__in": PRJ_CDs}
            fn122_cache = get_id_cache(Fnp.FN122, filters=filters)


            # =========================
            #        FN123

            data = prep.fn123(fn123, fn122_cache, spc_cache)
            items = []
            for item in data:
                obj = Fnp.FN123(**item)
                items.append(obj)
            Fnp.FN123.objects.bulk_create(items)
            filters = {"effort__sample__project__prj_cd__in": PRJ_CDs}
            fn123_cache = get_id_cache(Fnp.FN123, filters=filters)


            # =========================
            #        FN125

            data = prep.fn125(fn125, fn123_cache)
            items = []
            for item in data:
                obj = Fnp.FN125(**item)
                items.append(obj)
            Fnp.FN125.objects.bulk_create(items)
            filters = {"catch__effort__sample__project__prj_cd__in": PRJ_CDs}
            fn125_cache = get_id_cache(Fnp.FN125, filters=filters)


            # =========================
            #        FN125-Tags

            data = prep.fn125_tags(fn125tags, fn125_cache)
            items = []
            for item in data:
                obj = Fnp.FN125Tag(**item)
                items.append(obj)
            Fnp.FN125Tag.objects.bulk_create(items)

            # =========================
            #        FN125-Lamprey

            data = prep.fn125_lamprey(fn125lamprey, fn125_cache)
            items = []
            for item in data:
                obj = Fnp.FN125_Lamprey(**item)
                items.append(obj)
            Fnp.FN125_Lamprey.objects.bulk_create(items)


            # =========================
            #        FN126

            data = prep.fn126(fn126, fn125_cache)
            items = []
            for item in data:
                obj = Fnp.FN126(**item)
                items.append(obj)
            Fnp.FN126.objects.bulk_create(items)


            # =========================
            #        FN127

            data = prep.fn127(fn127, fn125_cache)
            items = []
            for item in data:
                obj = Fnp.FN127(**item)
                items.append(obj)
            Fnp.FN127.objects.bulk_create(items)

            return PRJ_CDs

    except DatabaseError:
        return "99"
