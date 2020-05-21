"""=============================================================
~/fn_portal/utils/get_gear_tables_from_fn_portal.py
 Created: 09 Aug 2019 09:26:23

 DESCRIPTION:

  This script migrates the gear data from one instance of fn_portal to
  another.  The database connections are made with psycopg2 rather than
  through the django orm.

  Generally this script will not need to be run very often, only when
  the fn_portal is being rebuilt of migrated from on platform to
  another.

 A. Cottrill
=============================================================

"""

import os
import sys
import psycopg2 as pg2


SRC_PARS = {
    "host": "142.143.160.56",
    "database": "fisheye",
    "user": "cottrillad",
    "password": "django",
}

TRG_PARS = {
    "host": "localhost",
    "database": "fn_portal",
    "user": "cottrillad",
    "password": "django123",
}

src_conn = pg2.connect(**SRC_PARS)
src_cursor = src_conn.cursor()

trg_conn = pg2.connect(**TRG_PARS)
trg_cursor = trg_conn.cursor()

# ==============================================
#                 USERS

print("Getting users ...")

sql = "select * from auth_user where username <> 'cottrillad';"
src_cursor.execute(sql)
rs = src_cursor.fetchall()

colnames = [x[0] for x in src_cursor.description]
colnames.pop(0)  # remove id

values = ", ".join(["%({})s".format(x) for x in colnames])
columns = ", ".join(colnames)

sql = "insert into auth_user ({}) values ({})".format(columns, values)

record_dicts = [{k: v for k, v in zip(colnames, record[1:])} for record in rs]
trg_cursor.executemany(sql, tuple(record_dicts))

trg_conn.commit()

# ==============================================
#              GEAR FAMILY

print("Getting gear families...")

sql = "select * from fn_portal_gearfamily;"
src_cursor.execute(sql)
rs = src_cursor.fetchall()

colnames = [x[0] for x in src_cursor.description]
colnames.pop(0)  # remove id

values = ", ".join(["%({})s".format(x) for x in colnames])
columns = ", ".join(colnames)

sql = "insert into fn_portal_gearfamily ({}) values ({})".format(columns, values)

record_dicts = [{k: v for k, v in zip(colnames, record[1:])} for record in rs]
trg_cursor.executemany(sql, tuple(record_dicts))

trg_conn.commit()


# ==============================================
#                 GEAR

print("Getting gears...")

# gear is a little more complicated because there are foreign keys to
# both users and gear family.

# we will need to create a map of family names and user names to their current ids


sql = "select id, abbrev from fn_portal_gearfamily"
src_cursor.execute(sql)
rs = src_cursor.fetchall()

gearfamily_map = {x[1]: x[0] for x in rs}


sql = "select id, username from auth_user"
src_cursor.execute(sql)
rs = src_cursor.fetchall()

user_map = {x[1]: x[0] for x in rs}

gear_map = {}

sql = """-- fk to family
SELECT family.abbrev as family, auth_user.username, gear.*
FROM fn_portal_gear AS gear
  join fn_portal_gearfamily AS family ON gear.family_id = family.id
  left join auth_user on auth_user.id=gear.assigned_to_id;
"""

src_cursor.execute(sql)
rs = src_cursor.fetchall()
colnames = [x[0] for x in src_cursor.description]

for record in rs:
    record_dict = {k: v for k, v in zip(colnames, record)}

    family = record_dict.pop("family")
    username = record_dict.pop("username")
    gear_id = record_dict.pop("id")

    record_dict["family_id"] = gearfamily_map.get(family)
    record_dict["assigned_to_id"] = user_map.get(username)

    values = ", ".join(["%({})s".format(x) for x in record_dict.keys()])
    columns = ", ".join(record_dict.keys())

    sql = "insert into fn_portal_gear ({}) values ({}) RETURNING id".format(
        columns, values
    )

    trg_cursor.execute(sql, record_dict)
    gear_map[gear_id] = trg_cursor.fetchone()[0]


trg_conn.commit()


# ==============================================
#                 SUBGEAR

print("Getting subgears...")
# repeat for subgear, creating a map of old_id's to new_ids for our subgears.

subgear_map = {}

sql = """select family.abbrev as family, subgear.* from
  fn_portal_subgear as subgear
  join fn_portal_gearfamily AS family ON subgear.family_id = family.id;"""

src_cursor.execute(sql)
rs = src_cursor.fetchall()
colnames = [x[0] for x in src_cursor.description]

for record in rs:
    record_dict = {k: v for k, v in zip(colnames, record)}

    family = record_dict.pop("family")
    subgear_id = record_dict.pop("id")

    record_dict["family_id"] = gearfamily_map.get(family)

    values = ", ".join(["%({})s".format(x) for x in record_dict.keys()])
    columns = ", ".join(record_dict.keys())

    sql = "insert into fn_portal_subgear ({}) values ({}) RETURNING id".format(
        columns, values
    )

    trg_cursor.execute(sql, record_dict)
    subgear_map[subgear_id] = trg_cursor.fetchone()[0]


trg_conn.commit()


# ==============================================
#             GEAR2SUBGEAR

print("Updating gear-subgear associations")

# Now get all of hte vlaues from gear2subgear and insert new records
# using our gear_map and subgear_map dictionaries to ensure the m2m
# relationships are maintained.

sql = """select panel_sequence, panel_count, gear_id, subgear_id
         from fn_portal_gear2subgear;"""

src_cursor.execute(sql)
rs = src_cursor.fetchall()
colnames = [x[0] for x in src_cursor.description]

# create a tuple of dictionaries with the new gear and subgear ids:
record_dicts = []

for record in rs:
    record_dict = {k: v for k, v in zip(colnames, record)}
    old_gear_id = record_dict["gear_id"]
    old_subgear_id = record_dict["subgear_id"]
    record_dict["gear_id"] = gear_map[old_gear_id]
    record_dict["subgear_id"] = subgear_map[old_subgear_id]
    record_dicts.append(record_dict)

values = ", ".join(["%({})s".format(x) for x in record_dict.keys()])
columns = ", ".join(record_dict.keys())

sql = "insert into fn_portal_gear2subgear ({}) values ({})".format(columns, values)

trg_cursor.executemany(sql, tuple(record_dicts))

trg_conn.commit()
trg_conn.close()
src_conn.close()


print("Done!")
