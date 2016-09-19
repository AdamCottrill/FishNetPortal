'''=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_offshore_data.py
Created: 10 Aug 2016 14:00:31


DESCRIPTION:

This scripts uses an associated access databaes
(~/fn_portal/utils/mdbs/Offshore.mdb) to convert the Lake Huron
Offshore master database to the fn_portal data model and create
associated objects for each record.  Similar databases can be (or have
been) created for other master datasets.  The database schema of both
is very close to the FishNet-II data model so very little conversion
is necessary although the FN_portal schema does not use compound
fields in child tables and is currently limited to only the most basic
fields in each table (there are often many redundant/empty fields in
many of the master data sets).



A. Cottrill
=============================================================

'''


import os
import sys
import pyodbc
#from collections import OrderedDict
#from copy import copy
#from utils.fn_portal_utils import *
#


SETTINGS_FILE = 'main.settings.local'

#SECRET should be set when virtualenv as activated.  Just incase its not
os.environ['SECRET_KEY'] = "\xb1>\xf3\x10\xd3p\x07\x8fS\x94'\xe3g\xc6cZ4\xb0R"

#taken from manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", SETTINGS_FILE)


# Type these:
import django
django.setup()
import django_settings

from django.db import IntegrityError

from fn_portal.models import (Species, FN011, FN121, FN122, FN123,
                              FN125, FN127, FN_Tags)


SRC_DB = "C:/1work/Python/djcode/fn_portal/utils/mdbs/Offshore.mdb"
LOOKUP_DB = "C:/1work/Data_Warehouse/LookupTables.mdb"
TRG_DB = 'c:/1work/Python/djcode/fn_portal/db/fn_portal.db'



#=======================================================
#                SPECIES:

what = "Species"
table = 'fn_portal_species'

sql = ('select int(spc) as species_code, spc_nm as common_name,' +
       'spc_nmsc as scientific_name from [SPC]')

print('Retrieving {} records...'.format(what))

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % LOOKUP_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute(sql)
    data = rs.fetchall()
    flds = [x[0] for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), what))

my_list = []
for x in data:
    row = {k:v for k,v in zip(flds, x)}
    my_list.append(Species(**row))

Species.objects.bulk_create(my_list)
print('Done adding {} records (n={:,})'.format(what, len(my_list)))



#=======================================================
#                FN011 - Projects
what = "Project"
my_list = []

print('Retrieving {} records...'.format(what))
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn011')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN011'))

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    prj_cd = row['prj_cd']
    row['slug'] = prj_cd.lower()
    my_list.append(FN011(**row))

FN011.objects.bulk_create(my_list)
print('Done adding {} records (n={:,})'.format(what, len(my_list)))

#=======================================================
#                FN121 - Samples/Net Sets

what = "Sample/Net Set"
my_list = []
print('Retrieving {} records...'.format(what))
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn121')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN121'))

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    prj_cd = row.get('prj_cd')
    try:
        project = FN011.objects.get(prj_cd=row.get('prj_cd'))
    except:
        msg = "Could not find project with prj_cd = {}"
        print(msg.format(prj_cd))
        next
    del row['prj_cd']
    row['project'] = project
    my_list.append(FN121(**row))
FN121.objects.bulk_create(my_list)
print('Done adding {} records (n={:,})'.format(what, len(my_list)))


#=======================================================
#                FN122 - Efforts
what = "Effort"
my_list = []
key_fields = ['prj_cd', 'sam']
print('Retrieving {} records...'.format(what))

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn122')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN122'))


for x in data:
    row = {k:v for k,v in zip(flds, x)}
    try:
        prj_cd = row.get('prj_cd')
        sam = row.get('sam')
        sample = FN121.objects.filter(project__prj_cd=prj_cd,
                                      sam__iexact=sam).get()
    except:
        msg = "Could not find sample with prj_cd = {} and sam = {}"
        print(msg.format(prj_cd, sam))
        next
    for keyfld  in key_fields:
        del row[keyfld]
    row['sample'] = sample
    my_list.append(FN122(**row))

FN122.objects.bulk_create(my_list)

print('Done adding {} records (n={:,})'.format(what, len(my_list)))

#=======================================================
#                FN123 - Catch Counts

what = "Catch Counts"
my_list = []
key_fields = ['prj_cd', 'sam', 'eff', 'spc'] #form foreign keys
print('Retrieving {} records...'.format(what))
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn123')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN122'))

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    try:
        prj_cd = row.get('prj_cd')
        sam = row.get('sam')
        eff = row.get('eff')
        spc = row.get('spc')
        effort = FN122.objects.filter(sample__project__prj_cd=prj_cd,
                                      sample__sam__iexact=sam,
                                      eff=eff).get()
        species = Species.objects.get(species_code=spc)
    except:
        msg = "Could not find effort with prj_cd = {}, sam = {} and eff={}"
        print(msg.format(prj_cd, sam, eff))
        next
    for keyfld  in key_fields:
        del row[keyfld]

    #add the related django objects
    row['effort'] = effort
    row['species'] = species

    #create our catch count object and add it to our list
    my_list.append(FN123(**row))

FN123.objects.bulk_create(my_list)

print('Done adding {} records (n={:,})'.format(what, len(my_list)))

#=======================================================
#                FN125 - Fish Data

what = "Fish Samples"
my_list = []
#form foreign keys:
key_fields = ['prj_cd', 'sam', 'eff', 'spc', 'grp']

print('Retrieving {} records...'.format(what))

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn125')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN125'))

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    prj_cd = row.get('prj_cd')
    sam = row.get('sam')
    eff = row.get('eff')
    grp = row.get('grp')
    spc = row.get('spc')
    try:
        species = Species.objects.get(species_code=spc)
        catch = FN123.objects.filter(effort__sample__project__prj_cd=prj_cd,
                                     effort__sample__sam__iexact=sam,
                                     effort__eff=eff,
                                     grp=grp, species=species).get()
    except:
        msg = ("Could not find catch record with: \n\tprj_cd = {}\n" +
               "\tsam = {}\n\teff = {}\n\tgrp = {}\n\tspc = {}\n")
        print(msg.format(prj_cd, sam, eff, grp, spc))
        next

    for keyfld in key_fields:
        del row[keyfld]

    row['catch'] = catch

#    fish = FN125(**row)
#    try:
#        fish.save()
#    except IntegrityError as e:
#        fish_num = row.get('fish')
#        msg = ("Could not create fish record with: \n\tprj_cd = {}\n" +
#               "\tsam = {}\n\teff = {}\n\tgrp = {}\n\tspc = {}\n\tfish={}")
#        print(msg.format(prj_cd, sam, eff, grp, spc,fish_num))
#        next
#

    #create our fish sample object and add it to our list
    my_list.append(FN125(**row))
FN125.objects.bulk_create(my_list, batch_size=10000)

print('Done adding {} records (n={:,})'.format(what, len(my_list)))

#=======================================================
#                FN127 - Age Estimates

what = 'Age Estimates'
my_list = []
#form foreign keys:
key_fields = ['prj_cd', 'sam', 'eff', 'spc', 'grp', 'fish']

print('Retrieving {} records ...'.format(what))
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn127')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

msg = 'Found {:,} records.  Creating {} objects ...'
print(msg.format(len(data), 'FN127'))

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    prj_cd = row.get('prj_cd')
    sam = row.get('sam')
    eff = row.get('eff')
    grp = row.get('grp')
    spc = row.get('spc')
    fish = row.get('fish')
    try:
        species = Species.objects.get(species_code=spc)
        catch = FN123.objects.filter(effort__sample__project__prj_cd=prj_cd,
                                     effort__sample__sam__iexact=sam,
                                     effort__eff=eff,
                                     grp=grp, species=species).get()
        fish = FN125.objects.filter(catch=catch, fish=fish).get()
    except:
        msg = ("Could not find fish record with: \n\tprj_cd = {}\n" +
               "\tsam = {}\n\teff = {}\n\tgrp = {}\n\tspc = {}\n\tfish={}\n")
        print(msg.format(prj_cd, sam, eff, grp, spc, fish))
        next

    for keyfld in key_fields:
        del row[keyfld]

    row['fish'] = fish

    #create our fish sample object and add it to our list
    my_list.append(FN127(**row))


FN127.objects.bulk_create(my_list)

print('Done adding {} records (n={:,})'.format(what, len(my_list)))
