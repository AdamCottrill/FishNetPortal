"""=============================================================
~/fn_portal/utils/get_protocols_from_xls.py
 Created: 10 Jul 2019 16:25:36

DESCRIPTION:

This is a utility script that loads the protocals (labels and
accronyms) from the excel spreadsheet ~/utils/Protocols.xlsx.

For each row of the spreadsheet a FNProtocol object is created and
appended to a master list. this list is then inserted with a final
bulk_create.

This script must be run when fn_portal is intialized and must be
populated before fn011 records are populated.

A. Cottrill
=============================================================

"""

import os
import sys

import django_settings

from xlrd import open_workbook, cellname

from fn_portal.models import FNProtocol
from utils.fn_portal_utils import sheet2dict


XLS = (
    "c:/Users/COTTRILLAD/Documents/1work/Python/djcode/"
    + "fn_portal/utils/Protocols.xlsx"
)

book = open_workbook(XLS)

sheet = book.sheet_by_name("Sheet1")
protocols = sheet2dict(sheet)
objects = []
for row in protocols:
    # protocol = FNProtocol(label=row['label'], abbrev=row['abbrev'])
    protocol = FNProtocol(**row)
    objects.append(protocol)

FNProtocol.objects.bulk_create(objects)
