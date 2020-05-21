"""
=============================================================
c:/1work/Python/djcode/fn_portal/utils/fn_portal_utils.py
Created: 11 Aug 2016 14:11:10


DESCRIPTION:



A. Cottrill
=============================================================
"""

import sqlite3

import pyodbc


def get_user_attrs(prj_ldr):
    """take a username from a fishnet project and return the first and
    last name, a user address and an ontario email address."""
    attrs = {}

    names = prj_ldr.title().split()
    firstName = names[0]
    if len(names) > 1:
        lastName = names[1]
    else:
        lastName = ""
    attrs["first_name"] = firstName
    attrs["last_name"] = lastName
    attrs["email"] = "{}.{}@ontario.ca".format(firstName.lower(), lastName.lower())
    attrs["username"] = lastName.lower() + firstName.lower()[:2]

    return attrs


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


def get_fn_data(src_db, fn_table, year=None):
    """Get the data and fields from the query in the src database for the
    fish net table specified by fn_table.  Returns list of
    dictionaries - each element represents a single row returned by the query.

    Arguments:
    - `src_db`: full path the source database.
    - `fn_table`:  the name of the stored query that returns the data for
                   the specified fish net table

    """
    if year:
        sql = "execute get_{} @yr='{}'".format(fn_table, year)
    else:
        sql = "execute get_{}".format(fn_table)

    constring = "DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={}"
    with pyodbc.connect(constring.format(src_db)) as src_conn:
        src_cur = src_conn.cursor()
        rs = src_cur.execute(sql)
        data = rs.fetchall()
        flds = [x[0].lower() for x in src_cur.description]

    records = []
    for record in data:
        records.append({k: v for k, v in zip(flds, record)})

    return records


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


def sheet2dict(sheet):
    """A helper function to convert a workbook sheet to a list of
    dictionaries.  THis function assumes that the field names are in
    the top row of the spreadsheet.  Each row is then converted to a
    dictionary using those field names. The return value is a list of
    dictionaries corresponding to rows in the spreadsheet.

    Arguments:
    - `sheet`: a sxlrd shee object ( e.g. - book.sheet_by_name("Sheet1"))

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


def query_for_id(sql, keys, trg_db):
    """Execute the provided sql string on the target database. Issue a
    meaningful error message contianing keys_as_string if there is a
    problem.

    Arguments:

    - `sql`:a sql statement that is intended t oretrieve
    the id of a parent record.  The sql string should return a scalar
    value (id)

    - `keys_as_string`: nicely formatted string contianing the
    key-values pairs in sql

    - `trg_db`: path a sqlite database

    """

    # trg_conn = sqlite3.connect(trg_db, uri=True)
    # trg_cur = trg_conn.cursor()
    # rs = trg_cur.execute(sql)
    # try:
    #    id = rs.fetchone()[0]
    # except:
    #    msg = "Unable to find record with key values: \n{}"
    #    print(msg.format(keys))
    #    id = None
    # finally:
    #    trg_conn.close()
    # return id

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


# def get_project_id(prj_cd, trg_db):
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

    key_values = {k: v for k, v in record.items() if k in keys}
    tmp = ["\t{}:{}\n".format(k, v) for k, v in key_values.items()]
    keys_as_string = "".join(tmp)
    return keys_as_string


def get_species_id(spc, trg_db):
    """Get the id of for the species code from the species table in our
    target database.

    Arguments:
    - `spc`: a 3 digit FishNet-II species code.
    - `trg_db`: path to a sqlite database.

    """

    sql = "select id from fn_portal_species where spc={};"
    sql = sql.format(int(spc))
    keys_as_string = "spc: {}".format(spc)
    id = query_for_id(sql, keys_as_string, trg_db)
    return id


def get_project_id(record, trg_db):
    """Get the id of a FN011 record (parent), given an FN121 record.

    Arguments:
    - `record`: a dictionary representing a database row.
    - `trg_db`: path to a sqlite database.
    """

    # FN121
    keys = ["prj_cd"]

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

    # FN121
    keys = ["prj_cd", "sam"]

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

    # key fields for the FN122 table
    keys = ["prj_cd", "sam", "eff"]

    sql = """select fn122.id from fn_portal_fn122 as fn122
    join fn_portal_fn121 as fn121 on fn121.id=fn122.sample_id
    join fn_portal_fn011 as fn011 on fn011.id=fn121.project_id
    where fn011.prj_cd='{prj_cd}' and fn121.sam='{sam}' and fn122.eff='{eff}'"""

    keys_as_string = key_values_as_string(keys, record)
    id = query_for_id(sql.format(**record), keys_as_string, trg_db)

    return id
