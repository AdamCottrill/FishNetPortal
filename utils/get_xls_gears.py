"""=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_xls_gears.py
Created: 05 Oct 2016 09:03:19


DESCRIPTION:

THis script reads in the gear, subgear, gear family and gear2subgear
tables from the excel spreadsheet used to capture information from the
master databases.  These tables are then used to create django orm
instances which are subsequently saved.



A. Cottrill
=============================================================

"""

# the data for each table is currently contained in individual
# worksheets in a spreadsheet. sheet names match model names, the first
# row of each column matches field names.  For models with foreign
# keys, fields that form unique identifiers to related objects should
# be present.


import os
import sys

# import sqlite3


SETTINGS_FILE = "main.settings.local"

# SECRET should be set when virtualenv as activated.  Just incase it's not
os.environ["SECRET_KEY"] = "\xb1>\xf3\x10\xd3p\x07\x8fS\x94'\xe3g\xc6cZ4\xb0R"

# taken from manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)

# Type these:
import django

django.setup()
import django_settings

from fn_portal.models import *

from xlrd import open_workbook, cellname

XLS = "C:/1work/Python/djcode/fn_portal/utils/Gears.xlsx"

book = open_workbook(XLS)

print("sheets in this workbook: " + ", ".join(book.sheet_names()))


def sheet2dict(sheet):
    """A helper function to convert a workbook sheet to a list of
    dictionaries.  THis function assumes that the field names are in
    the top row of the spreadsheet.  Each row is then converted to a
    dictionary using those field names. The return value is a list of
    dictionaries corresponding to rows in the spreadsheet.

    Arguments:
    - `sheet`:

    """
    my_list = []

    for row_index in range(sheet.nrows):
        if row_index == 0:
            fields = [sheet.cell(0, x).value.strip() for x in range(sheet.ncols)]
        else:
            vals = [sheet.cell(row_index, x).value for x in range(sheet.ncols)]
            my_dict = {k: v for k, v in zip(fields, vals)}
            my_list.append(my_dict)

    return my_list


sheet = book.sheet_by_name("GearFamily")
gear_families = sheet2dict(sheet)

sheet = book.sheet_by_name("GEAR")
gears = sheet2dict(sheet)

sheet = book.sheet_by_name("SubGear_GL")
subgears = sheet2dict(sheet)

sheet = book.sheet_by_name("gear2subgear")
gear2subgears = sheet2dict(sheet)


# Ok - now lets add our data

# first gear Families:

for family in gear_families:
    gearfamily = GearFamily(
        family=family.get("family"),
        abbrev=family.get("abbrev"),
        gear_type=family.get("gear_type"),
    )
    gearfamily.save()


def get_or_none(d, fld):
    """A little helper function to replace accessing dictionary keys and
    checking for empty strings.

    Arguments:
    - `dict`:
    - `fields`:

    """
    return d.get(fld) if d.get(fld) != "" else None


Gear.objects.all().delete()
for gear in gears:
    family = GearFamily.objects.get(abbrev=gear["family"])
    my_gear = Gear(
        family=family,
        gr_label=(gear["gr_label"]).title(),
        gr_code=gear["gr_code"],
        effcnt=get_or_none(gear, "effcnt"),
        effdst=get_or_none(gear, "effdst"),
        gr_des=gear["gr_des"],
    )
    my_gear.save()

# now add our subgears:


for x in subgears:
    family = GearFamily.objects.get(abbrev=x["family"])
    subgear = SubGear(
        family=family,
        eff=get_or_none(x, "EFF"),
        mesh=get_or_none(x, "Mesh Size"),
        grlen=get_or_none(x, "Panel Length"),
        grht=get_or_none(x, "Panel Height"),
        grcol=6,
        grmat=1,
        gryarn=1,
        grknot=2,
        grdiam=get_or_none(x, "Mesh Diameter"),
        tielength=get_or_none(x, "Length Of Ties"),
        meshes_per_tie=get_or_none(x, "Meshes Per Tie"),
        meshes_deep=get_or_none(x, "Meshes Deep"),
        eff_des=get_or_none(x, "Comment"),
    )
    subgear.save()


# now we need to associated each subgear with the appropriate gear
# i.e. - 'build-a-net'
for x in gear2subgears:
    my_family = GearFamily.objects.get(abbrev=x["family"])
    my_gear = Gear.objects.get(family=my_family, gr_code=x["GR"])
    my_subgear = SubGear.objects.get(family=my_family, eff=x["EFF"])

    gear2subgear = Gear2SubGear(
        gear=my_gear,
        subgear=my_subgear,
        panel_count=x["panel_count"],
        panel_sequence=x["panel_order"],
    )
    gear2subgear.save()
