'''=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_nearshore_data.py
Created: 10 Aug 2016 14:00:31


DESCRIPTION:

This scripts uses an associated access databaes
(~/fn_portal/utils/mdbs/Nearshore.mdb) to convert the Lake Huron
Nearshore master database to the fn_portal data model and create
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


SETTINGS_FILE = 'main.settings.append_data_local'

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


#SRC_DB = "C:/1work/Python/djcode/fn_portal/utils/mdbs/Nearshore.mdb"
SRC_DB = "C:/1work/Python/djcode/fn_portal/utils/mdbs/smallfish.mdb"
LOOKUP_DB = "C:/1work/Data_Warehouse/LookupTables.mdb"


data_sources = [
#    {'name':'offshore',
#     'SRC_DB': "C:/1work/Python/djcode/fn_portal/utils/mdbs/Offshore.mdb"},

    {'name':'nearshore',
     'SRC_DB':"C:/1work/Python/djcode/fn_portal/utils/mdbs/Nearshore.mdb"},

    {'name':'smallfish',
     'SRC_DB':"C:/1work/Python/djcode/fn_portal/utils/mdbs/smallfish.mdb"}

]



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

msg = '\tFound {:,} records.  Creating {} objects ...'
print(msg.format(len(data), what))

my_list = []
for x in data:
    row = {k:v for k,v in zip(flds, x)}
    my_list.append(Species(**row))

Species.objects.bulk_create(my_list)
print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))


#=======================================================
# now loop over our data source list and append the data from each in turn.

for source in data_sources:
    data_source = source['name']
    SRC_DB = source['SRC_DB']

    print("=" * 40 + "\nAdding data from {}".format(data_source))

    #=======================================================
    #                FN011 - Projects

    what = "Project"
    fn_table = 'FN011'
    my_list = []

    print('Retrieving {} records...'.format(what))
    constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
    with pyodbc.connect(constring) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute('execute get_fn011')
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    msg = '\tFound {:,} records.  Creating {} objects ...'
    print(msg.format(len(data), fn_table))

    for x in data:
        row = {k:v for k,v in zip(flds, x)}
        prj_cd = row['prj_cd']
        row['slug'] = prj_cd.lower()
        my_list.append(FN011(**row))

    FN011.objects.bulk_create(my_list, batch_size=10000)
    print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))


    #=======================================================
    #                FN121 - Samples/Net Sets

    what = "Sample/Net Set"
    fn_table = 'FN121'
    my_list = []
    print('Retrieving {} records...'.format(what))
    constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
    with pyodbc.connect(constring) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute('execute get_fn121')
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    msg = '\tFound {:,} records.  Creating {} objects ...'
    print(msg.format(len(data), fn_table))

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
        #del row['site'] #until we add site to our database
        row['project'] = project
        my_list.append(FN121(**row))
    FN121.objects.bulk_create(my_list, batch_size=10000)
    print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))





    #=======================================================
    #                FN122 - Efforts
    what = "Effort"
    fn_table = 'FN122'
    my_list = []
    key_fields = ['prj_cd', 'sam']
    print('Retrieving {} records...'.format(what))

    constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
    with pyodbc.connect(constring) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute('execute get_fn122')
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    msg = '\tFound {:,} records.  Creating {} objects ...'
    print(msg.format(len(data), fn_table))


    for x in data:
        row = {k:v for k,v in zip(flds, x)}
        try:
            prj_cd = row.get('prj_cd')
            sam = str(row.get('sam'))
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

    FN122.objects.bulk_create(my_list, batch_size=10000)

    print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))


    #in order for the cpue calculations to work, we also need
    # add one record to the 123 table for every fn122 record.
    # set SPC='000'
    my_list = []
    species = Species.objects.get(species_code='000')
    for x in data:
        row = {k:v for k,v in zip(flds, x)}

        prj_cd = row['prj_cd']
        sam = row['sam']
        eff = row['eff']
        effort = FN122.objects.get(sample__project__prj_cd=prj_cd,
                                   sample__sam=sam, eff=eff)
        my_list.append(FN123(effort=effort, species=species))
    FN123.objects.bulk_create(my_list, batch_size=10000)

    print('\tDone adding catch count placeholders for SPC=000')


    #=======================================================
    #                FN123 - Catch Counts

    what = "Catch Counts"
    fn_table = 'FN123'

    my_list = []
    key_fields = ['prj_cd', 'sam', 'eff', 'spc'] #form foreign keys
    print('Retrieving {} records...'.format(what))
    constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
    with pyodbc.connect(constring) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute('execute get_fn123')
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    msg = '\tFound {:,} records.  Creating {} objects ...'
    print(msg.format(len(data), fn_table))

    for x in data:
        row = {k:v for k,v in zip(flds, x)}
        try:
            prj_cd = row.get('prj_cd')
            sam = str(row.get('sam'))
            eff = row.get('eff')
            spc = row.get('spc')
            effort = FN122.objects.filter(sample__project__prj_cd=prj_cd,
                                          sample__sam__iexact=sam,
                                          eff=eff).get()
            species = Species.objects.get(species_code=spc)
        except:
            msg = "Could not find effort with prj_cd = {}, sam = {} and eff = {}"
            print(msg.format(prj_cd, sam, eff))
            next
        for keyfld  in key_fields:
            del row[keyfld]

        #add the related django objects
        row['effort'] = effort
        row['species'] = species

        #create our catch count object and add it to our list
        my_list.append(FN123(**row))

    FN123.objects.bulk_create(my_list, batch_size=10000)

    print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))


    #=======================================================
    #                FN125 - Fish Data

    what = "Fish Samples"
    fn_table = "FN125"
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

    msg = '\tFound {:,} records.  Creating {} objects ...'
    print(msg.format(len(data), fn_table))

    for x in data:
        row = {k:v for k,v in zip(flds, x)}
        prj_cd = row.get('prj_cd')
        sam = str(row.get('sam'))
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

        #create our fish sample object and add it to our list
        my_list.append(FN125(**row))


    FN125.objects.bulk_create(my_list, batch_size=10000)

    print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))



    #=======================================================
    #                FN127 - Age Estimates

    if data_source != 'smallfish':
        what = 'Age Estimates'
        fn_table = 'FN127'
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

        msg = '\tFound {:,} records.  Creating {} objects ...'
        print(msg.format(len(data), fn_table))

        for x in data:
            row = {k:v for k,v in zip(flds, x)}
            prj_cd = row.get('prj_cd')
            sam = str(row.get('sam'))
            eff = row.get('eff')
            grp = row.get('grp')
            spc = row.get('spc')
            fish = row.get('fish')
            row['accepted'] = row['accepted'] in ('Yes', -1, '-1', True, 'True')
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


        FN127.objects.bulk_create(my_list, batch_size=10000)

        print('\tDone adding {} records (n={:,})'.format(what, len(my_list)))



#=================================================
#             MISSING FLENs

#now update any missing flens with estimated values based on their tlen
#and species specific flen-tlen coefficient

#ideally this would be done in the database query get_fn125 before
#appending to fn_portal database - the query was causing duplicate
#records in both the nearshore and offshore databases (but not in
#small fish?).

#get flen-tlen regression coefficients:
what = "Flen2Tlen coefficients"

sql = ('select int(spc), intercept, slope from Flen2Tlen_lookup ' +
       'where slope is not null;')

print('Retrieving {} records...'.format(what))

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % LOOKUP_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute(sql)
    flen2tlen = rs.fetchall()


msg = '\tFound {:,} records.  Creating {} objects ...'
print(msg.format(len(flen2tlen), what))

for spc in flen2tlen:
    spc_code = spc[0]
    intercept = spc[1]
    slope = spc[2]

    fish = FN125.objects.filter(catch__species__species_code=spc_code).\
           filter(flen__isnull=True).exclude(tlen__isnull=True).all()
    if fish:
        for x in fish:
            x.flen = (x.tlen - intercept) / slope
            x.save()
print('Done populating missing fork lengths.')
