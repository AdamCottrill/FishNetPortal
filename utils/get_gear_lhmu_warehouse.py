"""=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_gear_lhmu_warehouse.py
Created: 26 Sep 2016 13:26:16

DESCRIPTION:

this script gets the gear data from the FN013 and FN014 tables and
appends it into corresponding tables in the FN_portal

A. Cottrill
=============================================================

"""


import os
import sys
import sqlite3

import django_settings

from fn_portal.models import FN011, FN013, FN014

# SRC_DB = 'C:/1work/ScrapBook/lhmu_warehouse.db'
SRC_DB = (
    "c:/Users/COTTRILLAD/OneDrive - Government of Ontario/Documents/"
    + "1work/ScrapBook/lhmu_warehouse.db"
)

src_conn = sqlite3.connect(SRC_DB)
src_cur = src_conn.cursor()

# ============================
#           FN013

sql = "select distinct prj_cd, gr, effcnt, effdst, gr_des from fn013"

src_cur.execute(sql)
rs = src_cur.fetchall()

# now loop over our records and see if there is a matching project in
# our fn011 table. If so, add the record to the FN013 table. If not,
# log the missing project code and drive on for now.

missing_prj_cds = []
objects = []

for record in rs:
    try:
        project = FN011.objects.get(prj_cd=record[0])
        foo = FN013(
            project=project,
            gr=record[1],
            effcnt=None if record[2] == "" else record[2],
            effdst=None if record[3] == "" else record[3],
            gr_des=record[4],
        )
        objects.append(foo)
    except FN011.DoesNotExist:
        missing_prj_cds.append(record[0])

FN013.objects.bulk_create(objects)
print("Done adding FN013 records.")

missing_prj_cds = set(missing_prj_cds)
# ============================
#           FN014


sql = """select distinct prj_cd, gr, eff, mesh, grlen, grht, grwid, grcol, grmat,
         gryarn, grknot, eff_des from fn014;"""

src_cur.execute(sql)
rs = src_cur.fetchall()


missing_grs = []
objects = []

for record in rs:
    gear = FN013.objects.filter(project__prj_cd=record[0], gr=record[1]).first()
    if gear:
        try:

            foo = FN014(
                gear=gear,
                eff=record[2],
                mesh=None if record[3] == "" else record[3],
                grlen=None if record[4] == "" else record[4],
                grht=None if record[5] == "" else record[5],
                grwid=None if record[6] == "" else record[6],
                grcol=record[7],
                grmat=record[8],
                gryarn=None if record[9] == "" else record[9],
                grknot=None if record[10] == "" else record[10],
                eff_des=record[11],
            )
            objects.append(foo)
        except FN013.DoesNotExist:
            missing_grs.append((record[0], record[1]))
            gear = None
    else:
        missing_grs.append((record[0], record[1]))
        gear = None


FN014.objects.bulk_create(objects)

print("Done adding FN014 records.")

missing_grs = list(set(missing_grs))

foo = FN013.objects.filter(project__prj_cd="LHA_IA00_002").all()

src_cur.close()
src_conn.close()
