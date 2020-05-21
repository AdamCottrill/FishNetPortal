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

- make sure to run ~/utils/get_protocols_from_xls.py first and ensure
  that species has been populated - these two steps should only be
  necessary if the database is being rebuild from scratch.

USAGE:

- to rebuild everything, leave FIRST_YEAR and LAST_YEAR set to
  None. To get specific years, specify a two element array containing
  first and last years to refresh or replace.

- if only FIRST_YEAR is defined, all years >= FIRST_YEAR will be updated.

- if only LAST_YEAR is defined, all years <= FIRST_YEAR will be updated.

- if both FIRST_YEAR and LAST_YEAR are defined, all years >= FIRST_YEAR
  and <= LAST_YEAR will be updated.

this script assumes that the source databases have existing queries
named get_<table> for all of the FN tables. If the datasource does not
include that table (lamprey in small fish), queries with the
appropriate name must still exist, but return no records.


TODOS:

- update Lake Superior FCIN database
- update other Lake Superior databases when they become available


 A. Cottrill
=============================================================

"""
import os
import pyodbc
import re
import sys
import django_settings

from django.contrib.auth import get_user_model


from common.models import Species, Grid5, Lake

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


from utils.fn_portal_utils import (
    get_user_attrs,
    get_db_years,
    get_fn_data,
    build_years_array,
)


# HOMEDIR = (
#     "c:/Users/COTTRILLAD/OneDrive - Government of Ontario/Documents/"
#     + "1work/Python/djcode/fn_portal"
# )

User = get_user_model()
HOMEDIR = os.path.expandvars("${HOME}/Python/djcode/apps/fn_portal")

DB_DIR = os.path.join(HOMEDIR, "utils/mdbs")

# year or None
FIRST_YEAR = 2019
LAST_YEAR = None

DATA_SOURCES = [
    # {"name": "nearshore", "src_db": "Nearshore.accdb", "lake_abbrev": "HU"},
    # {"name": "offshore", "src_db": "Offshore.accdb", "lake_abbrev": "HU"},
    # {"name": "smallfish", "src_db": "smallfish.accdb", "lake_abbrev": "HU"},
    {"name": "offshore", "src_db": "SuperiorOffshore.accdb", "lake_abbrev": "SU"}
]


# users
# check our users before we go any farther:

users = {}

for source in DATA_SOURCES:
    src_db = os.path.join(DB_DIR, source["src_db"])
    fndata = get_fn_data(src_db, "project_leads")

    for rec in fndata:
        prj_ldr = rec["prj_ldr"].upper()
        users[prj_ldr] = get_user_attrs(prj_ldr)


# there are a couple of duplicate entries we need to address:

users["ADAM COTTRILL / JEFF SPEERS"] = users.get("ADAM COTTRILL")
users["DAVIS / COTTRILL / SPEERS"] = users.get("JEFF SPEERS")
users["LAKE HURON RESEARCH"] = users.get("BRIAN HENDERSON")
users["STEPHEN GILES"] = users.get("STEPHEN GILE")
users["STEVE GILE"] = users.get("STEPHEN GILE")
users["Vicki Lee and Adam Cottrill"] = users.get("VICKI LEE")

# now loop over all of our users and get or create each user.  When we
# get our user back, add it as the value to our user cache so we can
# add the relationship when we create the FN011 record.

user_cache = {}
for key, attrs in users.items():
    if attrs:
        user, created = User.objects.get_or_create(username=attrs["username"])
        if created:
            for attr, value in attrs.items():
                setattr(user, attr, value)
            user.save()
        user_cache[key.upper()] = user


# Protocols Lookup:
protocols = {x.abbrev: x for x in FNProtocol.objects.all()}


species_cache = {x.spc: x for x in Species.objects.all()}

lake_cache = {x.abbrev: x for x in Lake.objects.all()}
grid_cache = {x.slug: x for x in Grid5.objects.all()}

# =======================================================================


for source in DATA_SOURCES:

    src_db = os.path.join(DB_DIR, source["src_db"])
    if not os.path.isfile(src_db):
        print("*** ERROR ***: Unable to find '{}'".format(source.get("src_db")))
        break

    source_name = source["name"]
    lake = lake_cache[source["lake_abbrev"]]

    # create a cursor that will be used to connect to our source database:
    years = get_db_years(src_db)
    years = build_years_array(years, FIRST_YEAR, LAST_YEAR)

    # clear out all of the old objects:
    print("Clearing tables from selected years and sources...")
    FN011.objects.filter(year__in=years, source=source_name, lake=lake).delete()
    print("Done clearing tables...")

    for year in years:

        # =======================================================
        #                FN011 - Projects

        print("\n====================================================")

        what = "Project"
        fn_table = "FN011"
        obj_list = []

        # get the data
        print("Retrieving {} records for {}...".format(what, year))
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
            row["lake"] = lake
            prj_ldr = row["prj_ldr"].upper()
            row["prj_ldr"] = user_cache[prj_ldr]
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
            x.slug: x
            for x in FN011.objects.filter(year=year, source=source_name, lake=lake)
        }

        # get the data
        print("Retrieving {} records...".format(what))
        fndata = get_fn_data(src_db, fn_table, year)
        msg = "\tFound {:,} records.  Creating {} objects ..."
        print(msg.format(len(fndata), fn_table))

        for row in fndata:
            prj_cd = row.pop("prj_cd")
            grid_no = int(row.pop("grid"))
            grid_slug = "{0}-{1:04d}".format(lake.abbrev.lower(), grid_no)
            row["grid"] = grid_cache[grid_slug]

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
                project__year=year, project__source=source_name, project__lake=lake
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
                sample__project__year=year,
                sample__project__lake=lake,
                sample__project__source=source_name,
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

            species = species_cache[spc]

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
                effort=effort, slug=slug + "-000-00", species=species_cache["000"]
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
                catch__effort__sample__project__lake=lake,
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
            fish_lam_id = row.pop("fish_lam_id")
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

            # some data sources have individual rows for each wound already
            # they will have a value for fish_lam_id
            if fish_lam_id:
                row["lamid"] = fish_lam_id
                row["slug"] = "{}-{}".format(parent_slug, row["lamid"]).lower()
                obj_list.append(FN125_Lamprey(**row))

            elif lamijc == "0":
                row["lamid"] = 1
                row["slug"] = "{}-{}".format(parent_slug, row["lamid"]).lower()
                row["lamijc"] = "0"
                row["lamijc_type"] = "0"
                obj_list.append(FN125_Lamprey(**row))
            else:
                # split lamijc on every A or B and parse them into rows:
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

        # ===========================================================

        # finally update our flag fields for the records we just added:
        print("Updating tag_flag in the FN125 records...")
        FN125.objects.filter(catch__effort__sample__project__year__in=years).filter(
            catch__effort__sample__project__source__in=source_name
        ).filter(fishtags__in=FN125Tag.objects.all()).update(tag_flag=True)

        print("Updating lam_flag in the FN125 records...")
        FN125.objects.filter(catch__effort__sample__project__year__in=years).filter(
            catch__effort__sample__project__source__in=source_name
        ).filter(lamprey_marks__in=FN125_Lamprey.objects.all()).update(lam_flag=True)

        print("Updating stom_flag in the FN125 records...")
        FN125.objects.filter(catch__effort__sample__project__year__in=years).filter(
            catch__effort__sample__project__source__in=source_name
        ).filter(diet_data__in=FN126.objects.all()).update(stom_flag=True)

        print("Updating age_flag in the FN125 records...")
        FN125.objects.filter(catch__effort__sample__project__year__in=years).filter(
            catch__effort__sample__project__source__in=source_name
        ).filter(age_estimates__in=FN127.objects.all()).update(age_flag=True)

print("Done!")
