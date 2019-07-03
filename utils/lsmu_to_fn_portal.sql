--- the queries in this script will return the records sets need to convert the lake Superior 
-- data warehouse into the FN_portal format.
-- at this point no attempt is made to check for orphans or duplicates or verify any of the data values.

--- get_fn011
select case when 
    cast(substr(prj_cd,7,2) as integer) < 50 
    then '20' || substr(prj_cd,7,2) 
    else '19' || substr(prj_cd,7,2) end as yr,
    prj_cd, 
    prj_nm, 
    prj_ldr, 
    prj_date0, 
    prj_date1, 
    'superior' as lake, 
    'superior' as source, 
    comment0 from fn011 limit 50;


-- get_fn121

select prj_cd, sam, effdt0, efftm0, effdt1, efftm1, effdur, effst, grtp, gr, X_orient as orient, sidep, grid, my_ddlon as dd_lon, my_ddlat as dd_lat, comment1, Null as secchi from fn121_w_spatial limit 10;


-- get_fn122
select PRJ_CD, SAM, EFF, EFFDST, GRDEPMIN as GRDEP, GRTEM as GRTEM0, NULL as GRTEM1 from fn122;

-- get_fn123
--select * from fn123 limit 10;
select PRJ_CD, SAM, case when eff is null then '001' else eff end as eff, GRP, CATCNT, BIOCNT, null as Comment from fn123 limit 10;

-- get_fn125
select prj_cd, 
sam, 
case when eff is null then '001' else eff end as eff, 
spc, 
case when grp is null then '001' else grp end as grp, 
fish, flen, tlen, rwt, sex, mat, gon, clipc, girth, agest, null as NODA, NODC, FATE, comment5 
from fn125 limit 10;

-- get 127 from 125
--select * from fn125 limit 10;
select prj_cd, sam, case when eff is null then '001' else eff end as eff, spc, case when grp is null then '00' else grp end as grp, fish, 125 as ageid, age as agea, 'Yes' as accepted, '99999' as AGEMT, '99' as XAGEM, null as conf, null as NCA, null as edge, null as comment7 from fn125 where age is not null and age <> '' 
union all
-- get 127 from 127
--select * from fn127 limit 10;
select prj_cd, sam, case when eff is null then '001' else eff end as eff, spc, case when grp is null then '00' else grp end as grp, fish, ageid, agea, 'No' as accepted, AGEMT, '99' as XAGEM, conf, NCA, edge, null as comment7 from fn127;
