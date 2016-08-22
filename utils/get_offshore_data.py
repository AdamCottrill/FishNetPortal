'''
=============================================================
c:/1work/Python/djcode/fn_portal/utils/get_offshore_data.py
Created: 10 Aug 2016 14:00:31


DESCRIPTION:



A. Cottrill
=============================================================
'''


import pyodbc
import sqlite3
from collections import OrderedDict
from copy import copy
from utils.fn_portal_utils import *



SRC_DB = "C:/1work/Data_Warehouse/IA_OFFSHORE.mdb"
LOOKUP_DB = "C:/1work/Data_Warehouse/LookupTables.mdb"
TRG_DB = 'c:/1work/Python/djcode/fn_portal/db/fn_portal.db'

SRC_PREFIX = 'Offshore_'

#open a connection to our new target database:
#trg_conn = sqlite3.connect(TRG_DB)
#trg_cur = trg_conn.cursor()






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


fldcnt = len(flds)

sql2 = '''insert into {0}({1}) values({2}?)'''.format(
    table,
    ', '.join(['[{}]'.format(x) for x in flds]),
    "?," * (fldcnt-1))

with sqlite3.connect(TRG_DB) as trg_conn:
    trg_cur = trg_conn.cursor()
    trg_cur.executemany(sql2, data)
    trg_conn.commit()


#=======================================================
#                    FN011


table = 'fn011'
trg_table = 'fn_portal_{}'.format(table)

src_conn = pyodbc.connect(r"DRIVER={Microsoft Access Driver (*.mdb)};" \
                          "DBQ=%s" % SRC_DB)
src_cur = src_conn.cursor()



tmp = trg_cur.execute('select * from {} limit 0'.format(trg_table))
trg_fields = [x[0] for x in tmp.description]
trg_fields.pop(trg_fields.index('id'))


sql = 'select {0} from [{1}{2}]'.format(
    ','.join(['[{}]'.format(x) for x in trg_fields]),
    SRC_PREFIX, table)


rs = src_cur.execute(sql)
data = rs.fetchall()

fldcnt = len(trg_fields)

sql2 = '''insert into {0} ({1}) values({2}?)'''.format(
    trg_table,
    ', '.join(['[{}]'.format(x) for x in trg_fields]),
    "?," * (fldcnt-1))

with sqlite3.connect(TRG_DB) as trg_conn:
    trg_cur = trg_conn.cursor()
    trg_cur.executemany(sql2, data)
    trg_conn.commit()

#=======================================================
#                    FN121



table = 'FN121'

flds = ['prj_cd',
    'sam',
    'grid',
    'effdt0',
    'effdt1',
    'effdur',
    'efftm0',
    'efftm1',
    'effst',
    'gr',
    'orient',
    'sidep',
    'latlong',
    'siloc',
    'lat',
    'lon',
    'xy_type',
    'dd_lat',
    'dd_lon',
    'dd_lat2',
    'dd_lon2',
    'date',
    'grtp',
    'area',
    'site',
    'sitem',
    'xfishnam',
    'xgryarn',
    'xorient',
    'xset',
    'xstat',
    'spctrg',
    'comment1',
    'secchi',
    'xslime',]


sql = 'select {0} from [{1}{2}]'.format(
    ','.join(['[{}]'.format(x) for x in flds]),
    SRC_PREFIX, table)

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute(sql)
    records = rs.fetchall()

with sqlite3.connect(TRG_DB) as trg_conn:
    trg_cur = trg_conn.cursor()

    for record in records:
        tmp = OrderedDict(zip(flds, record))
        tmp['project_id'] = get_project_id(tmp['prj_cd'], TRG_DB)
        del tmp['prj_cd']

        sql2 = '''insert into [{}]({}) values ({});'''

        flds2 = [x for x in tmp.keys()]
        trg_table = 'fn_portal_{}'.format(table)

        jj = sql2.format(trg_table,
                         ', '.join(['[{}]'.format(x) for x in flds2]),
                         ', '.join([':' + x for x in flds2]),
        )

        trg_cur.execute(jj, tmp)
    trg_conn.commit()

print('Done adding FN121 records (n={})'.format(len(records)))


#=======================================================
#                    FN122

table = 'FN122'
trg_parent_key_field = 'sample_id'

parent_keys = ['prj_cd', 'sam',]
common_flds = [
    'eff',
    'effdst',
    'grdep',
    'grtem0',
    'grtem1',
    'stratum',
    'xeffday',
    'xeffdsta',
    'xeffdstb',
    'xgrdep',
    'xgrdepa',
    'xgrdepb',
    'xgrtem',
    'xgrtema',
    'xgrtemb',
    'xsidep',
    'xsidepa',
    'xsidepb',]


#123

table = 'FN123'
trg_parent_key_field = 'effort_id'

fk_fields = ['spc']

parent_keys = ['prj_cd', 'sam', 'eff']
common_flds = [
    #'spc',
    'grp',
    'catcnt',
    'biocnt',
    'kilcnt',
    'mrkcnt',
    'rcpcnt',
    'rlscnt',
    'catwt',
    'stratum',
    'xcatcnta',
    'xcatcntb',
    'xlntally',
    'xtally',
    'comment0',
    'comment3',
]

trg_table = 'fn_portal_{}'.format(table)
all_flds = parent_keys + fk_fields + common_flds

#get the data from our source database:
sql = 'select {0} from [{1}{2}]'.format(
    ','.join(['[{}]'.format(x) for x in all_flds]),
    SRC_PREFIX, table)

constring = r"DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s" % SRC_DB
with pyodbc.connect(constring) as src_conn:
    src_cur = src_conn.cursor()
    rs = src_cur.execute(sql)
    records = rs.fetchall()
    src_flds = [x[0] for x in src_cur.description]

# insert it into the target database
# for each row, we convert it to a dictionary, and get the id of the parent
# using the key fields and then remove those key fields from the dictionary
# the remaining data is appended to the db.

#with sqlite3.connect(TRG_DB) as trg_conn:
#    trg_cur = trg_conn.cursor()
#    for record in records:
#        tmp = OrderedDict(zip(all_flds, record))
#        tmp['sample_id'] = get_sample_id(tmp, TRG_DB)
#        for fld in parent_keys:
#            del tmp[fld]
#        sql2 = '''insert into [{}]({}) values ({});'''
#        flds2 = [x for x in tmp.keys()]
#        jj = sql2.format(trg_table,
#                         ', '.join(['[{}]'.format(x) for x in flds2]),
#                         ', '.join([':' + x for x in flds2]),
#        )
#
#        trg_cur.execute(jj, tmp)
#        trg_conn.commit()
#


#re-do the code above, but create a copy of records with the parent id
# at the end of each record. then loop over the new copy of records,
# pop off the key fields and then append the data using execute many.



key_index = [src_flds.index(x) for x in parent_keys]

if 'spc' in all_flds:
    spc_idx = all_flds.index('spc')

records2 = [list(x) for x in records]
for record in records2:
    key_dict = {k:record[v].upper() for k,v in zip(parent_keys, key_index)}
    if table == 'FN122':
        fk_id = get_sample_id(key_dict, TRG_DB)
    elif table == 'FN123':
        fk_id = get_effort_id(key_dict, TRG_DB)
    else:
        #fn125
        fk_id = get_catch_id(key_dict, TRG_DB)

    record.append(fk_id)
    if 'spc' in all_flds:
        spc_id = get_species_id(record[spc_idx], TRG_DB)
        record.append(spc_id)
        for i in sorted(key_index + [spc_idx], reverse=True):
            del record[i]
    else:
        for i in sorted(key_index, reverse=True):
            del record[i]


#modify the field names too:
#remove the fields associated with the parent key
#add the new foreign key name to end:
all_flds2 = copy(all_flds)
all_flds2.append(trg_parent_key_field)
for i in sorted(key_index, reverse=True):
    del all_flds2[i]

if 'spc' in all_flds2:
    del all_flds2[all_flds2.index('spc')]
    all_flds2.append('species_id')


#now build our sql string using all_flds2

sql2 = '''insert into [{}]({}) values ({});'''

sql2run = sql2.format(trg_table,
                 ', '.join(['[{}]'.format(x) for x in all_flds2]),
                      ', '.join('?' * len(all_flds2))
)


with sqlite3.connect(TRG_DB) as trg_conn:
    trg_cur = trg_conn.cursor()
    trg_cur.executemany(sql2run, records2)
    trg_conn.commit()
print('Done adding {} records (n={})'.format(table, len(records)))


#FN123



#FN125


#
