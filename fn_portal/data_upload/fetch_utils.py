"""
=============================================================
~\fn_portal\data_upload\fetch_utils.py
Created: Aug-12-2021 09:43
DESCRIPTION:

    fetch FN011
    fetch FN013
    fetch FN014
    fetch FN022
    fetch FN026
    fetch FN028
    fetch FN121


A. Cottrill
=============================================================
"""


# an example of connecting to MS Access with SQL Alchemy
# and reflecting it to get the tables and columns and running a simple
# query.


import pyodbc


def get_mdb_connection(mdb):
    """

    Arguments:
    - `mdb`: path to either a *.mdb or *.accdb file.

    """
    constring = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s"
    con = pyodbc.connect(constring % mdb)
    return con


def execute_select(con, stmt):

    dat = []
    with con.cursor() as cursor:
        cursor.execute(stmt)
        rs = cursor.fetchall()
        colnames = [x[0].lower() for x in cursor.description]
        for row in rs:
            row_dict = {k: v for k, v in zip(colnames, row)}
            dat.append(row_dict)
    return dat


def get_fn011_stmt():

    stmt = """select
        YEAR,
        PRJ_CD,
        PRJ_NM,
        PRJ_LDR,
        PRJ_DATE0,
        PRJ_DATE1,
        COMMENT0,
        PROTOCOL,
        LAKE from FN011"""

    return stmt


def get_fn022_stmt():

    stmt = """select
                PRJ_CD,
                SSN,
                SSN_DES,
                SSN_DATE0,
                SSN_DATE1
         from FN022"""

    return stmt


def get_fn026_stmt():

    stmt = """select
             PRJ_CD,
             SPACE,
             SPACE_DES,
             SITE_LST,
             SITP_LST,
             AREA_LST,
             SIDEP_LT,
             SIDEP_GE,
             GRDEP_LT,
             GRDEP_GE
         from FN026"""
    return stmt


def get_fn028_stmt():

    stmt = """select
                PRJ_CD,
                MODE,
                MODE_DES,
                GR,
                GRUSE,
                ORIENT,
                EFFDUR_GE,
                EFFDUR_LT,
                EFFTM0_GE,
                EFFTM0_LT
         from FN028"""
    return stmt


def get_fn013_stmt():

    stmt = """select
                PRJ_CD,
                GR,
                GRTP,
                GR_DES,
                EFFCNT,
                EFFDST
         from FN013"""
    return stmt


def get_fn014_stmt():

    stmt = """select
                PRJ_CD,
                GR,
                EFF,
                EFF_DES,
                MESH,
                GRLEN,
                GRHT,
                GRWID,
                GRCOL,
                GRMAT,
                GRYARN,
                GRKNOT
         from FN014"""
    return stmt


def get_fn121_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                SSN,
                SPACE,
                MODE,
                EFFDT0,
                EFFTM0,
                EFFDT1,
                EFFTM1,
                EFFDUR,
                EFFST,
                SITP,
                SITE,
                GRID5,
                DD_LAT0 as DD_LAT,
                DD_LON0 as DD_LON,
                DD_LAT1,
                DD_LON1,
                SITEM,
                SITEM1,
                SITEM0,
                SIDEP,
                GRDEPMAX,
                GRDEPMIN,
                SECCHI,
                XSLIME,
                CREW,
                COMMENT1
         from FN121"""
    return stmt


def get_fn122_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                EFFDST,
                GRDEP,
                GRTEM0,
                GRTEM1,
                WATERHAUL,
                COMMENT2
         from FN122"""
    return stmt


def get_fn123_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                CATCNT,
                BIOCNT,
                CATWT,
                SUBCNT,
                SUBWT,
                COMMENT3 as COMMENT
         from FN123"""
    return stmt


def get_fn124_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                SIZ,
                SIZCNT
         from FN124"""
    return stmt


def get_fn125_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FLEN,
                TLEN,
                GIRTH,
                RWT,
                SEX,
                MAT,
                GON,
                CLIPC,
                CLIPA,
                NODC,
                NODA,
                TISSUE,
                AGEST,
                FATE,
                AGE_FLAG,
                LAM_FLAG,
                STOM_FLAG,
                TAG_FLAG,
                COMMENT5
         from FN125"""
    return stmt


def get_fn125tags_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FISH_TAG_ID,
                TAGID,
                TAGDOC,
                TAGSTAT,
                XCWTSEQ,
                XTAGINCKD,
                COMMENT_TAG
         from FN125_tags"""
    return stmt


def get_fn125lamprey_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                LAMID,
                XLAM,
                LAMIJC_TYPE,
                LAMIJC_SIZE,
                COMMENT_LAM
         from FN125_lamprey"""
    return stmt


def get_fn126_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                FOOD,
                TAXON,
                FDCNT,
                FDMES,
                FDVAL,
                LF,
                COMMENT6
         from FN126"""
    return stmt


def get_fn127_stmt():

    stmt = """select
                PRJ_CD,
                SAM,
                EFF,
                SPC,
                GRP,
                FISH,
                AGEID,
                PREFERRED,
                AGEA,
                XAGEM,
                AGEMT,
                EDGE,
                CONF,
                NCA,
                COMMENT7
         from FN127"""
    return stmt
