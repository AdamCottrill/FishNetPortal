"""=============================================================
~/fn_portal/utils/get_fn2_data.py
 Created: 11 Jul 2019 09:59:05

DESCRIPTION:

This script is used to rebuild the data in FN portal from the MS
access databases that are currently used as the master databases for
the offshore, nearshore and small fish programs in both lakes Huron
and Superior.

Three globals control what data is inserted into the fn_portal
database: FIRST_YEAR, LAST_YEAR, and SOURCE.

**NOTE** - before any data is appended to the database, all data
  matching the criteria is purged from FN_portal and completely
  replaced with new data returned from the selected source(s).


This script replaces all earlier scripts that were origially used to
get data from offshore, nearshore, and smallfish databases.

- make sure to run ~/utils/get_protocols_from_xls.py first.

USAGE:

- to rebuild everything, leave FIRST_YEAR and LAST_YEAR set to
  None. To get specific years, specify a two element array containing
  first and last years to refresh or replace.

- if only FIRST_YEAR is defined, all years >= FIRST_YEAR will be updated.

- if only LAST_YEAR is defined, all years <= FIRST_YEAR will be updated.

- if both FIRST_YEAR and LAST_YEAR are defined, all years >= FIRST_YEAR
  and <= LAST_YEAR will be updated.



 A. Cottrill
=============================================================

"""
import os
import pyodbc
import re

import django_settings

from fn_portal.models import Species

from fn_portal.models import (
    FNProtocol,
    FN011,
    FN121,
    FN122,
    FN123,
    FN125,
    FN126,
    FN127,
    FN125Tag,
    FN125_Lamprey,
)

DB_DIR = "C:/Users/COTTRILLAD/Documents/1work/Python/djcode/fn_portal/utils/mdbs"

FIRST_YEAR = 2004
LAST_YEAR = None

DATA_SOURCES = [
    {"name": "nearshore", "src_db": "Nearshore.mdb"},
    # {"name": "offshore", "src_db": "Offshore.mdb"},
    # {"name": "smallfish", "src_db": "smallfish.mdb"},
]


# Protocols Lookup:
protocols = {x.abbrev: x for x in FNProtocol.objects.all()}

species_lookup = {"{:03d}".format(x.species_code): x for x in Species.objects.all()}

# =======================================================================


def build_years_array(db_years, first_year=None, last_year=None):
    """The database queries are parameterized to accept a single year of
    data.  This function takes a two element array [db_years] (which
    contains year first and last years in the target database) and two
    optional arguments that specify the earliest and latest year to
    subset that array by.  returns an array of years that encapsulate
    the years inthe database, subsetted by the provided first_year and
    last_year parameters.

    Arguments:
    - `db_years`: [min([year]), max([year])]
    - `first_year`:
    - `last_year`:

    """

    fyear = max(first_year, db_years[0]) if first_year else db_years[0]
    lyear = min(last_year, db_years[1]) if last_year else db_years[1]

    return list(range(fyear, lyear + 1))


def get_db_years(src_db):
    """connect to our source database and get the first and last year in
    the fn011 table. (first and last year in the fn011 table are returned
    by a stored query [get_db_years] that must exist in the database).

    Arguments:
    - `src_db`: full path the source database.

    """

    constring = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
    with pyodbc.connect(constring.format(src_db)) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute("execute get_db_years")
        yrs = rs.fetchone()
    return [int(x) for x in yrs]


def get_fn_data(src_db, fn_table, year):
    """Get the data and fields from the query in the src database for the
    fish net table specified by fn_table.  Returns list of
    dictionaries - each element represents a single row returned by the query.

    Arguments:
    - `src_db`: full path the source database.
    - `fn_table`:  the name of the stored query that returns the data for
                   the specified fish net table

    """

    constring = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
    with pyodbc.connect(constring.format(src_db)) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute("execute get_{} @yr='{}'".format(fn_table, year))
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    records = []
    for record in data:
        records.append({k: v for k, v in zip(flds, record)})

    return records


# =======================================================================


# # =======================================================================
# # THIS IS TEMPORARY!
# # REMOVE ONCE UGLMU_COMMON COMES ON LINE!!!
#
#
# LOOKUP_DB = "C:/1work/Data_Warehouse/LookupTables.mdb"
#
# what = "Species"
# table = "fn_portal_species"
#
# sql = (
#     "select int(spc) as species_code, spc_nm as common_name,"
#     + "spc_nmsc as scientific_name from [SPC]"
# )
#
# print("Retrieving {} records...".format(what))
#
# constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % LOOKUP_DB
# with pyodbc.connect(constring) as src_conn:
#     src_cur = src_conn.cursor()
#     rs = src_cur.execute(sql)
#     data = rs.fetchall()
#     flds = [x[0] for x in src_cur.description]
#
# msg = "\tFound {:,} records.  Creating {} objects ..."
# print(msg.format(len(data), what))
#
# my_list = []
# for x in data:
#     row = {k: v for k, v in zip(flds, x)}
#     my_list.append(Species(**row))
#
# Species.objects.bulk_create(my_list)
# print("\tDone adding {} records (n={:,})".format(what, len(my_list)))
#

# =======================================================================


for source in DATA_SOURCES:

    src_db = os.path.join(DB_DIR, source["src_db"])
    source_name = source["name"]

    # create a cursor that will be used to connect to our source database:
    years = get_db_years(src_db)
    years = build_years_array(years, FIRST_YEAR, LAST_YEAR)

    # clear out all of the old objects:
    print("Clearing tables....")
    FN011.objects.filter(year__in=years, source=source_name).delete()
    print("Done clearing tables...")

    for year in years:
        # year = 2014

        # =======================================================
        #                FN011 - Projects

        what = "Project"
        fn_table = "FN011"
        obj_list = []

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        # add, remove or update any values here and append to our list of
        # objects to create:
        for row in fndata:
            prj_cd = row["prj_cd"]
            row["slug"] = prj_cd.lower()
            protocol = row.pop("protocol")
            row["protocol"] = protocols[protocol]
            obj_list.append(FN011(**row))

        FN011.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN121 - Samples/Net Sets

        what = "Sample/Net Set"
        fn_table = "FN121"
        obj_list = []

        parents = {
            x.slug: x for x in FN011.objects.filter(year=year, source=source_name)
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            project = parents.get(prj_cd.lower())
            if project is None:
                msg = "Could not find project with prj_cd = {}"
                print(msg.format(prj_cd.lower()))
                next
            row["project"] = project
            row["slug"] = "{}-{}".format(prj_cd, row["sam"]).lower()
            obj_list.append(FN121(**row))
        FN121.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN122 - EFFORTS

        what = "Effort"
        fn_table = "FN122"
        obj_list = []

        parents = {
            x.slug: x
            for x in FN121.objects.filter(
                project__year=year, project__source=source_name
            )
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            parent_slug = "-".join([prj_cd, sam]).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find sample with slug = {}"
                print(msg.format(parent_slug))
                next
            row["sample"] = parent
            row["slug"] = "-".join([parent_slug, row["eff"]]).lower()
            obj_list.append(FN122(**row))
        FN122.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN123 - Catch Counts

        what = "Catch Counts"
        fn_table = "FN123"
        obj_list = []

        parents = {
            x.slug: x
            for x in FN122.objects.filter(
                sample__project__year=year, sample__project__source=source_name
            )
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")

            species = species_lookup[spc]

            parent_slug = "-".join([prj_cd, sam, eff]).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find effort with slug = {}"
                print(msg.format(parent_slug))
                next
            row["slug"] = "{}-{}-{}".format(parent_slug, spc, row["grp"]).lower()

            # add the related django objects
            row["effort"] = parent
            row["species"] = species

            obj_list.append(FN123(**row))
        FN123.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        obj_list = []

        for slug, effort in parents.items():
            tmp = FN123(
                effort=effort, slug=slug + "-000-00", species=species_lookup["000"]
            )
            obj_list.append(tmp)
        FN123.objects.bulk_create(obj_list, batch_size=10000)

        print("\tDone adding catch count placeholders for SPC=000")

        # =======================================================
        #                FN125 - Fish Data

        what = "Fish Samples"
        fn_table = "FN125"
        obj_list = []

        parents = {
            x.slug: x
            for x in FN123.objects.filter(
                effort__sample__project__year=year,
                effort__sample__project__source=source_name,
            )
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")

            parent_slug = "{}-{}-{}-{}-{}".format(prj_cd, sam, eff, spc, grp).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find catch with slug = {}"
                print(msg.format(parent_slug))
                next
            row["slug"] = "{}-{}".format(parent_slug, row["fish"]).lower()
            # add the related django objects
            row["catch"] = parent
            row["comment5"] = None if row["comment5"] is None else row["comment5"][:500]
            obj_list.append(FN125(**row))
        FN125.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN127 - Age Estimates

        what = "Age Estimates"
        fn_table = "FN127"

        obj_list = []

        parents = {
            x.slug: x
            for x in FN125.objects.filter(
                catch__effort__sample__project__year=year,
                catch__effort__sample__project__source=source_name,
            )
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")
            fish = row.pop("fish")
            parent_slug = "{}-{}-{}-{}-{}-{}".format(
                prj_cd, sam, eff, spc, grp, fish
            ).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find fish with slug = {}"
                print(msg.format(parent_slug))
                next
            row["preferred"] = True if row["preferred"].lower() == "yes" else False
            row["slug"] = "{}-{}".format(parent_slug, row["ageid"]).lower()
            # add the related django objects
            row["fish"] = parent
            obj_list.append(FN127(**row))
        FN127.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN126 - FIELD DIET ANALYSIS

        what = "Diet Items"
        fn_table = "FN126"

        obj_list = []

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            year = row.pop("year")
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")
            fish = row.pop("fish")
            # work around:
            row["foodcnt"] = row.pop("fdcnt")

            parent_slug = "{}-{}-{}-{}-{}-{}".format(
                prj_cd, sam, eff, spc, grp, fish
            ).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find fish with slug = {}"
                print(msg.format(parent_slug))
                next
            row["slug"] = "{}-{}".format(parent_slug, row["food"]).lower()
            # add the related django objects
            row["fish"] = parent
            obj_list.append(FN126(**row))
        FN126.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                FN125_TAGS

        what = "TAGS"
        fn_table = "tags"

        obj_list = []

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")
            fish = row.pop("fish")

            parent_slug = "{}-{}-{}-{}-{}-{}".format(
                prj_cd, sam, eff, spc, grp, fish
            ).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find fish with slug = {}"
                print(msg.format(parent_slug))
                next
            row["slug"] = "{}-{}".format(parent_slug, row["fish_tag_id"]).lower()
            # add the related django objects
            row["fish"] = parent
            obj_list.append(FN125Tag(**row))
        FN125Tag.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        # =======================================================
        #                LAMPREY - XLAM then LAMIJC

        what = "XLAM"
        fn_table = "xlam"

        obj_list = []

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")
            fish = row.pop("fish")

            parent_slug = "{}-{}-{}-{}-{}-{}".format(
                prj_cd, sam, eff, spc, grp, fish
            ).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find fish with slug = {}"
                print(msg.format(parent_slug))
                next
            row["slug"] = "{}-{}".format(parent_slug, row["lamid"]).lower()
            # add the related django objects
            row["fish"] = parent
            obj_list.append(FN125_Lamprey(**row))
        FN125_Lamprey.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )

        what = "LAMIJC"
        fn_table = "lamijc"

        obj_list = []

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            sam = row.pop("sam")
            eff = row.pop("eff")
            spc = row.pop("spc")
            grp = row.pop("grp")
            fish = row.pop("fish")
            lamijc = row.pop("lamijc")

            parent_slug = "{}-{}-{}-{}-{}-{}".format(
                prj_cd, sam, eff, spc, grp, fish
            ).lower()
            parent = parents.get(parent_slug)
            if parent is None:
                msg = "Could not find fish with slug = {}"
                print(msg.format(parent_slug))
                next
            # add the related django objects
            row["fish"] = parent

            if lamijc == "0":
                row["lamid"] = 1
                row["slug"] = "{}-{}".format(parent_slug, row["lamid"]).lower()
                row["lamijc"] = "0"
                row["lamijc_type"] = "0"
                obj_list.append(FN125_Lamprey(**row))
            else:
                for i, wound in enumerate(re.findall("([(A|B)]\d+)", lamijc)):
                    row["lamijc"] = wound
                    row["lamid"] = i + 1
                    row["slug"] = "{}-{}".format(parent_slug, row["lamid"]).lower()
                    row["lamijc_type"] = wound[:2].upper()
                    row["lamijc_size"] = None if wound[2:] == "" else int(wound[2:])
                    obj_list.append(FN125_Lamprey(**row))

        FN125_Lamprey.objects.bulk_create(obj_list, batch_size=10000)
        print(
            "\tDone adding {} records for {} (n={:,})".format(what, year, len(obj_list))
        )


# finally update our flag fields:
FN125.objects.filter(fishtags__in=FN125Tag.objects.all()).update(tag_flag=True)
FN125.objects.filter(lamprey_marks__in=FN125_Lamprey.objects.all()).update(
    stom_flag=True
)
FN125.objects.filter(diet_data__in=FN126.objects.all()).update(stom_flag=True)
FN125.objects.filter(age_estimates__in=FN127.objects.all()).update(age_flag=True)
