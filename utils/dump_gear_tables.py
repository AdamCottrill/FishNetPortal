"""
=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/utils/dump_gear_tables.py
 Created: 20 May 2020 12:52:22

 DESCRIPTION:



 A. Cottrill
=============================================================
"""
import os
import csv
import psycopg2 as pg2

OUTDIR = "c:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/utils/gear_tables"


PG_PARS = {
    "host": "localhost",
    "database": "fn_portal",
    "user": "cottrillad",
    "password": "django123",
}


def get_data(sql, pg_pars):

    pg_conn = pg2.connect(**pg_pars)
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute(sql)
    rs = pg_cursor.fetchall()
    colnames = [x[0] for x in pg_cursor.description]
    pg_conn.close()

    return {"colnames": colnames, "data": rs}


queries = [
    {
        "fname": "FN013.csv",
        "sql": """
 -- FN013
-- fk to FN011
SELECT prj_cd,
       fn013.*
FROM fn_portal_fn013 AS FN013
  JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn013.project_id;

  """,
    },
    {
        "fname": "FN014.csv",
        "sql": """
-- FN014
SELECT project.prj_cd,
       gear.gr,
       fn014.*
FROM fn_portal_fn014 AS fn014
  JOIN fn_portal_fn013 AS gear ON gear.id = fn014.gear_id
  JOIN fn_portal_fn011 AS project ON project.id = gear.project_id;
""",
    },
    {
        "fname": "gear_family.csv",
        "sql": """
-- GEAR FAMILY
select * from fn_portal_gearfamily;
""",
    },
    {
        "fname": "users.csv",
        "sql": """
-- fk to User
-- users:
SELECT id,
       username,
       first_name,
       last_name,
       email
FROM auth_user
WHERE username <> 'cottrillad';
""",
    },
    {
        "fname": "gear.csv",
        "sql": """
-- GEAR
SELECT family.abbrev AS family,
       auth_user.username as assigened_to,
       gear.*
FROM fn_portal_gear AS gear
  JOIN fn_portal_gearfamily AS family ON gear.family_id = family.id
  LEFT JOIN auth_user ON auth_user.id = gear.assigned_to_id;
""",
    },
    {
        "fname": "subgear.csv",
        "sql": """
-- SUBGEAR
select family.abbrev as family, subgear.* from
  fn_portal_subgear as subgear
  join fn_portal_gearfamily AS family ON subgear.family_id = family.id;
""",
    },
    {
        "fname": "gear2subgear.csv",
        "sql": """
-- Gear2SubGear
select panel_sequence, panel_count, gear_id, subgear_id
         from fn_portal_gear2subgear;
""",
    },
]


for query in queries:
    print(query["fname"])
    fname = os.path.join(OUTDIR, query["fname"])
    data = get_data(query["sql"], PG_PARS)

    with open(fname, "a", newline="") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"')
        writer.writerow(data["colnames"])
        writer.writerows(data["data"])

print("Done!")
