'''
=============================================================
c:/1work/Python/djcode/fn_portal/utils/fn_portal_utils.py
Created: 11 Aug 2016 14:11:10


DESCRIPTION:



A. Cottrill
=============================================================
'''

import sqlite3

def query_for_id(sql, keys, trg_db):
    """Execute the provided sql string on the target database. Issue a
    meaningful error message contianing keys_as_string if there is a
    problem.

    Arguments:

    - `sql`:a sql statement that is intended to retrieve
    the id of a parent record.  The sql string should return a scalar
    value (id)

    - `keys_as_string`: nicely formatted string contianing the
    key-values pairs in sql

    - `trg_db`: path a sqlite database

    """

    #trg_conn = sqlite3.connect(trg_db, uri=True)
    #trg_cur = trg_conn.cursor()
    #rs = trg_cur.execute(sql)
    #try:
    #    id = rs.fetchone()[0]
    #except:
    #    msg = "Unable to find record with key values: \n{}"
    #    print(msg.format(keys))
    #    id = None
    #finally:
    #    trg_conn.close()
    #return id

    import sqlite3 as db
    with db.connect(trg_db) as trg_conn:
        trg_cur = trg_conn.cursor()
        try:
            rs = trg_cur.execute(sql)
            id = rs.fetchone()[0]
        except:
            msg = "Unable to find record with key values: \n{}"
            print(msg.format(keys))
            id = None
    return id



#def get_project_id(prj_cd, trg_db):
#    """
#
#    Arguments:
#    - `prj_cd`:
#    - `trg_db`:
#    """
#    trg_conn = sqlite3.connect(trg_db)
#    trg_cur = trg_conn.cursor()
#    rs = trg_cur.execute('select id from fn_portal_fn011 where prj_cd=?;',
#                         (prj_cd,))
#    project_id = rs.fetchone()[0]
#    trg_conn = sqlite3.connect(TRG_DB)
#    return project_id


def key_values_as_string(keys, record):
    """Given a dictionary representing a database record, return a nicely
    formatted string contianing the key-value pairs for all of the key
    fields contained in keys.

    """

    key_values = {k:v for k,v in record.items() if k in keys}
    tmp = ["\t{}:{}\n".format(k,v) for k, v in key_values.items()]
    keys_as_string = ''.join(tmp)
    return keys_as_string


def get_species_id(spc, trg_db):
    """Get the id of for the species code from the species table in our
    target database.

    Arguments:
    - `spc`: a 3 digit FishNet-II species code.
    - `trg_db`: path to a sqlite database.

    """

    sql = 'select id from fn_portal_species where species_code={};'
    sql = sql.format(int(spc))
    keys_as_string = 'species_code: {}'.format(spc)
    id = query_for_id(sql, keys_as_string, trg_db)
    return id



def get_project_id(record, trg_db):
    """Get the id of a FN011 record (parent), given an FN121 record.

    Arguments:
    - `record`: a dictionary representing a database row.
    - `trg_db`: path to a sqlite database.
    """

    #FN121
    keys = ['prj_cd']

    sql = """select fn011.id from fn_portal_fn011 as fn011
     where fn011.prj_cd='{prj_cd}'"""

    keys_as_string = key_values_as_string(keys, record)
    id = query_for_id(sql.format(**record), keys_as_string, trg_db)
    return id


def get_sample_id(record, trg_db):
    """Get the id of a FN121 record (parent), given an FN122 record.

    Arguments:
    - `record`: a dictionary representing a database row.
    - `trg_db`: path to a sqlite database.
    """

    #FN121
    keys = ['prj_cd', 'sam']

    sql = """select fn121.id from fn_portal_fn121 as fn121
    join fn_portal_fn011 as fn011 on fn011.id=fn121.project_id
    where fn011.prj_cd='{prj_cd}' and fn121.sam='{sam}'"""

    keys_as_string = key_values_as_string(keys, record)

    id = query_for_id(sql.format(**record), keys_as_string, trg_db)
    return id


def get_effort_id(record, trg_db):
    """Get the id of a FN122 record (parent), given an FN123 record.

    Arguments:
    - `record`: a dictionary representing a database row from a FN123 table
    - `trg_db`: path to a sqlite database.
    """

    #key fields for the FN122 table
    keys = ['prj_cd', 'sam', 'eff']

    sql = """select fn122.id from fn_portal_fn122 as fn122
    join fn_portal_fn121 as fn121 on fn121.id=fn122.sample_id
    join fn_portal_fn011 as fn011 on fn011.id=fn121.project_id
    where fn011.prj_cd='{prj_cd}' and fn121.sam='{sam}' and fn122.eff='{eff}'"""

    keys_as_string = key_values_as_string(keys, record)
    id = query_for_id(sql.format(**record), keys_as_string, trg_db)

    return id
