"""=============================================================
~/fn_portal/utils/get_gear_from_csv.py
 Created: 20 May 2020 15:20:01


 DESCRIPTION:

  This script is the compliment to dump_gear_tables.py that exports
  all the gear tables into csv files.  This script reads them back
  into the database.

  Generally this script will not need to be run very often, only when
  the fn_portal is being rebuilt of migrated from on platform to
  another.

 A. Cottrill
=============================================================

"""

import os
import sys
import csv
import psycopg2 as pg2


DATADIR = "c:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/utils/gear_tables"

TRG_PARS = {
    "host": "localhost",
    "database": "gldjango",
    "user": "cottrillad",
    "password": "django123",
}


trg_conn = pg2.connect(**TRG_PARS)
trg_cursor = trg_conn.cursor()


def float_or_none(val):
    """

    Arguments:
    - `x`:
    """

    if val is None:
        return None
    elif val == "":
        return None
    else:
        return float(val)


def int_or_none(val, default=None):
    """

    Arguments:
    - `x`:
    """
    if val is None:
        if default is not None:
            return default
        else:
            return None
    elif val == "":
        if default is not None:
            return default
        else:
            return None
    else:
        return int(val)


# ==============================================
#              GEAR FAMILY

print("Getting gear families...")

fname = os.path.join(DATADIR, "gear_family.csv")

data = []
with open(fname, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        data.append(row)

colnames = data.pop(0)[1:]

# values = ", ".join(["'%({})'s".format(x) for x in colnames])
values = ",".join(["%s"] * len(colnames))
columns = ", ".join(colnames)

sql = "insert into fn_portal_gearfamily ({}) values ({})".format(columns, values)

trg_conn = pg2.connect(**TRG_PARS)
trg_cursor = trg_conn.cursor()


trg_cursor.executemany(sql, [x[1:] for x in data])

trg_conn.commit()


# ==============================================
#                 GEAR

print("Getting gears...")

# gear is a little more complicated because there are foreign keys to
# both users and gear family.

# we will need to create a map of family names and user names to their current ids


fname = os.path.join(DATADIR, "gear.csv")
data = []
with open(fname, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        data.append(row)

colnames = data.pop(0)


sql = "select id, abbrev from fn_portal_gearfamily"
trg_cursor.execute(sql)
rs = trg_cursor.fetchall()

gearfamily_map = {x[1]: x[0] for x in rs}


# sql = "select id, username from auth_user"
# trg_cursor.execute(sql)
# rs = trg_cursor.fetchall()

# user_map = {x[1]: x[0] for x in rs}


gear_map = {}

for record in data:
    record_dict = {k: v for k, v in zip(colnames, record)}

    family = record_dict.pop("family")
    username = record_dict.pop("assigned_to")
    gear_id = record_dict.pop("id")

    record_dict["family_id"] = gearfamily_map.get(family)
    record_dict["assigned_to_id"] = user_map.get(username)

    record_dict["effdst"] = float_or_none(record_dict["effdst"])
    record_dict["effcnt"] = int_or_none(record_dict["effcnt"])

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


fname = os.path.join(DATADIR, "subgear.csv")
data = []
with open(fname, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        data.append(row)

colnames = data.pop(0)


for record in data:

    record_dict = {k: v for k, v in zip(colnames, record)}

    family = record_dict.pop("family")
    subgear_id = record_dict.pop("id")
    eff = record_dict.pop("eff")
    eff_des = record_dict.pop("eff_des")

    # all of the other fields are numeric - so make sure they are
    for k, v in record_dict.items():
        record_dict[k] = float_or_none(record_dict[k])

    record_dict["family_id"] = gearfamily_map.get(family)
    record_dict["eff"] = eff
    record_dict["eff_des"] = eff_des

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

# Now get all of the values from gear2subgear and insert new records
# using our gear_map and subgear_map dictionaries to ensure the m2m
# relationships are maintained.


fname = os.path.join(DATADIR, "gear2subgear.csv")
data = []
with open(fname, newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
    for row in reader:
        data.append(row)

colnames = data.pop(0)


# create a tuple of dictionaries with the new gear and subgear ids:
record_dicts = []

for record in data:
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


print("Done adding gears and subgears!")


# ===================================================

# Update FN013 and FN014 after projects are updated.
