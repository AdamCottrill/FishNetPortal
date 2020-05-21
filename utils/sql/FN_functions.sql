-- this script contains a number of sql functions that emulate data contianed in a FishNet-II 
-- database.

-- NOTES:
-- species is in [fn_portal_species] (this may not alway be the case)


-- FN011 - project run in a year:
CREATE OR REPLACE FUNCTION fn011 (_year varchar) RETURNS TABLE (prj_cd varchar,prj_nm varchar,prj_ldr varchar,prj_date0 DATE,prj_date1 DATE,source varchar,lake varchar)
AS
$$
SELECT prj_cd,
       prj_nm,
       prj_ldr,
       DATE (prj_date0) AS prj_date0,
       DATE (prj_date1) AS prj_date1,
       source,
       lake
FROM fn_portal_fn011 AS fn011
WHERE FN011.year = _year $$ LANGUAGE 'sql';


CREATE OR REPLACE FUNCTION fn121 (_prj_cd varchar) RETURNS TABLE (prj_cd varchar,sam varchar,effdt0 DATE,effdt1 DATE,efftm0 TIME,efftm1 TIME,effdur float,effst varchar,grtp varchar,gr varchar,orient varchar,sidep float,sitem varchar,grid varchar,dd_lat float,dd_lon float,secchi float,comment1 varchar)
AS
$$
SELECT prj_cd,
       sam,
       DATE (effdt0) AS effdt0,
       DATE (effdt1) AS effdt1,
       efftm0::TIME AS efftm0,
       efftm1::TIME AS efftm1,
       effdur,
       effst,
       grtp,
       gr,
       orient,
       sidep,
       sitem,
       grid,
       dd_lat,
       dd_lon,
       secchi,
       comment1
FROM fn_portal_fn121 AS fn121
  JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id
WHERE fn011.prj_cd = _prj_cd
ORDER BY sam $$ LANGUAGE 'sql';

--DROP FUNCTION fn122 (varchar);

CREATE OR REPLACE FUNCTION fn122 (_prj_cd varchar) RETURNS TABLE (prj_cd varchar,eff varchar,effdst float,grdep float,grtem0 float,grtem1 float)
AS
$$
SELECT prj_cd,
       eff,
       effdst,
       grdep,
       grtem0,
       grtem1
FROM fn_portal_fn122 AS fn122
  JOIN fn_portal_fn121 AS fn121 ON fn121.id = fn122.sample_id
  JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id
WHERE fn011.prj_cd = _prj_cd
ORDER BY sam,
         eff $$ LANGUAGE 'sql';

--DROP FUNCTION FN123 (varchar);

CREATE OR REPLACE FUNCTION fn123 (_prj_cd varchar) RETURNS TABLE (prj_cd varchar,sam varchar,eff varchar,spc int,grp varchar,catcnt int,catwt float,biocnt int)
AS
$$
SELECT prj_cd,
       sam,
       eff,
       species.spc AS spc,
       grp,
       catcnt,
       catwt,
       biocnt
FROM fn_portal_fn123 AS fn123
  JOIN fn_portal_fn122 AS fn122 ON fn122.id = fn123.effort_id
  JOIN fn_portal_fn121 AS fn121 ON fn121.id = fn122.sample_id
  JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id
  JOIN common_species AS species ON species.id = fn123.species_id
WHERE fn011.prj_cd = _prj_cd
AND   species.spc != 0
ORDER BY sam,
         eff,
         species.spc,
         grp $$ LANGUAGE 'sql';


--DROP FUNCTION fn125 (varchar);

CREATE OR REPLACE FUNCTION fn125 (_prj_cd varchar) RETURNS TABLE (prj_cd varchar,sam varchar,eff varchar,spc int,grp varchar,fish varchar,tlen int,flen int,rwt int,girth int,clipc varchar,sex varchar,mat varchar,gon varchar,noda varchar,nodc varchar,agest varchar,fate varchar,comment5 varchar,agea int,xagem varchar,agemt varchar,lamijc varchar)
AS
$$
SELECT prj_cd,
       sam,
       eff,
       spc,
       grp,
       fish,
       tlen,
       flen,
       rwt,
       girth,
       clipc,
       sex,
       mat,
       gon,
       noda,
       nodc,
       fish.agest,
       fate,
       comment5,
       agea,
       xagem,
       agemt,
       lamijc
FROM (SELECT fn125.id AS fish_id,
             prj_cd,
             sam,
             eff,
             species.spc,
             grp,
             fish,
             tlen,
             flen,
             rwt,
             girth,
             clipc,
             sex,
             mat,
             gon,
             noda,
             nodc,
             agest,
             fate,
             comment5
      FROM fn_portal_fn125 AS fn125
        JOIN fn_portal_fn123 AS fn123 ON fn123.id = fn125.catch_id
        JOIN common_species AS species ON species.id = fn123.species_id
        JOIN fn_portal_fn122 AS fn122 ON fn122.id = fn123.effort_id
        JOIN fn_portal_fn121 AS fn121 ON fn121.id = fn122.sample_id
        JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id
      WHERE fn011.prj_cd = _prj_cd) AS fish
  LEFT JOIN (SELECT *
             FROM fn_portal_fn127
             WHERE fn_portal_fn127.preferred = TRUE) AS fn127 ON fish.fish_id = fn127.fish_id
  LEFT JOIN (SELECT fish_id,
                    STRING_AGG(lamijc,'') AS lamijc
             FROM fn_portal_fn125_lamprey
             GROUP BY fish_id) AS lamprey ON lamprey.fish_id = fish.fish_id

      ORDER BY fish.prj_cd,
               fish.sam,
               fish.eff,
               fish.spc,
               fish.grp,
               fish.fish             

 $$ LANGUAGE 'sql';

commit();

--select count(*) from FN011('2018');


--select agea as age, xagem, agemt from fn_portal_fn127 where accepted=true limit 10;

-- SELECT *
-- FROM fn011 ('2012');




-- SELECT *
-- FROM fn121 ('LHA_IA18_002');

-- SELECT *
-- FROM fn122 ('LHA_IA18_002');

-- SELECT *
-- FROM fn123 ('LHA_IA18_002');

-- SELECT *
-- FROM fn125 ('LHA_IA18_002');


-- SELECT fish.*,
--        agea,
--        xagem,
--        agemt,
--        lamijc
-- FROM (SELECT fn125.id AS fish_id,
--              prj_cd,
--              sam,
--              eff,
--              species.spc,
--              grp,
--              fish,
--              tlen,
--              flen,
--              rwt,
--              girth,
--              clipc,
--              sex,
--              mat,
--              gon,
--              noda,
--              nodc,
--              agest,
--              fate,
--              comment5
--       FROM fn_portal_fn125 AS fn125
--         JOIN fn_portal_fn123 AS fn123 ON fn123.id = fn125.catch_id
--         JOIN common_species AS species ON species.id = fn123.species_id
--         JOIN fn_portal_fn122 AS fn122 ON fn122.id = fn123.effort_id
--         JOIN fn_portal_fn121 AS fn121 ON fn121.id = fn122.sample_id
--         JOIN fn_portal_fn011 AS fn011 ON fn011.id = fn121.project_id
--       WHERE fn011.prj_cd = 'LHA_IA18_007'
--       ORDER BY prj_cd,
--                sam,
--                eff,
--                species.spc,
--                grp,
--                fish) AS fish
--   LEFT JOIN (SELECT *
--              FROM fn_portal_fn127
--              WHERE fn_portal_fn127.preferred = TRUE) AS fn127 ON fish.fish_id = fn127.fish_id
--   LEFT JOIN (SELECT fish_id,
--                     STRING_AGG(lamijc,'') AS lamijc
--              FROM fn_portal_fn125_lamprey
--              GROUP BY fish_id) AS lamprey ON lamprey.fish_id = fish.fish_id


-- select * from fn_portal_fn121 limit 10;
-- select * from fn_portal_species limit 10;
-- select * from fn_portal_fn127 limit 10;
-- select fish_id, string_agg(lamijc, '') as lamijc from fn_portal_fn125_lamprey group by fish_id;


-- select * from fn011('2011');
--select * from fn_portal_species limit 10;
