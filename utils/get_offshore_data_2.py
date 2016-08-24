'''
=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_offshore_data.py
Created: 10 Aug 2016 14:00:31


DESCRIPTION:



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

from fn_portal.models import (Species, FN011, FN121, FN122, FN123,
                              FN125, FN127, FN_Tags)


SRC_DB = "C:/1work/Python/djcode/fn_portal/utils/mdbs/Offshore.mdb"
LOOKUP_DB = "C:/1work/Data_Warehouse/LookupTables.mdb"
TRG_DB = 'c:/1work/Python/djcode/fn_portal/db/fn_portal.db'



#=======================================================
#                SPECIES:


table = 'fn_portal_species'

sql = ('select int(spc) as species_code, spc_nm as common_name,' +
       'spc_nmsc as scientific_name from [SPC]')

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % LOOKUP_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute(sql)
    data = rs.fetchall()
    flds = [x[0] for x in src_cur.description]


my_list = []
for x in data:
    row = {k:v for k,v in zip(flds, x)}
    my_list.append(Species(**row))
Species.objects.bulk_create(my_list)
print('Done Adding Species (n={})'.format(len(data)))


#=======================================================
#                FN011
my_list = []

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn011')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    my_list.append(FN011(**row))
#    project = FN011(**row)
#    project.save()
FN011.objects.bulk_create(my_list)
print('Done adding projects (n={})'.format(len(data)))

#=======================================================
#                FN121

my_list = []
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn121')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    try:
        prj_cd = row.get('prj_cd')
        project = FN011.objects.get(prj_cd=row.get('prj_cd'))
    except:
        msg = "Could not find project with prj_cd = {}"
        print(msg.format(prj_cd))
        next
    del row['prj_cd']
    row['project'] = project
    my_list.append(FN121(**row))
FN121.objects.bulk_create(my_list)
print('Done adding net sets (n={})'.format(len(data)))


#=======================================================
#                FN122

my_list = []
constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn122')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

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
    del row['prj_cd']
    del row['sam']
    row['sample'] = sample
    my_list.append(FN122(**row))

FN122.objects.bulk_create(my_list)

print('Done adding net efforts (n={})'.format(len(data)))


#=======================================================
#                FN123

my_list = []

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute('execute get_fn123')
    data = rs.fetchall()
    flds = [x[0].lower() for x in src_cur.description]

for x in data:
    row = {k:v for k,v in zip(flds, x)}
    try:
        prj_cd = row.get('prj_cd')
        sam = row.get('sam')
        eff = row.get('eff')
        spc = row.get('spc')
        effort = FN122.objects.filter(sample__project__prj_cd=prj_cd,
                                      sample__sam=sam,
                                      eff=eff).get()
        species = Species.objects.get(species_code=spc)
    except:
        msg = "Could not find effort with prj_cd = {}, sam = {} and eff={}"
        print(msg.format(prj_cd, sam, eff))
        next
    #remove the key fields from our dictionary
    del row['prj_cd']
    del row['sam']
    del row['eff']
    del row['spc']

    #add the related django objects
    row['effort'] = effort
    row['species'] = species

    #create our catch count object and add it to our list
    my_list.append(FN123(**row))

FN123.objects.bulk_create(my_list)

print('Done adding net catch counts (n={})'.format(len(data)))
