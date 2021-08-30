-- select prj_cd, mode, gr, grtp, gruse, orient, count(prj_cd) as N from fn121
-- group by prj_cd, mode, gr, grtp, gruse, orient
-- having prj_cd like 'LHA_IA96_%';
-- select distinct prj_cd,
-- mode,
-- gr,
-- ifnull(grtp, substr(gr,1,2)),
-- ifnull(gruse, iif(gruse='',1,gruse) gruse,
-- ifnull(orient, 1) orient
-- from fn121
-- where prj_cd like 'LHA_IA98_%';
--
select distinct PRJ_CD,
    mode,
    CASE
        WHEN GR = ''
        OR GR is null THEN 'GL99'
        ELSE GR
    END AS gr,
    CASE
        WHEN GR = ''
        OR GR is null THEN 'XX'
        ELSE ifnull(grtp, substr(gr, 1, 2))
    END AS grtp,
    CASE
        WHEN gruse = '' THEN 9
        ELSE ifnull(GRUSE, 9)
    END AS gruse,
    CASE
        WHEN orient = '' THEN 9
        ELSE ifnull(ORIENT, 9)
    END AS orient
from fn121
where prj_cd like 'LHA_IA98_%' --    select
    --prj_cd,
    --sam,
    --stratum,
    --area,
    --grid,
    --site,
    --mode,
    --gr,
    --grtp,
    --gruse,
    --orient,
    --effst,
    --grdep,
    --grdepmax,
    --grdepmin,
    --sidep,
    --sitp,
    --sitran,
    --effdt0,
    --efftm0,
    --effdt1,
    --efftm1,
    --effdur
    --
    --    from fn121 where prj_cd like 'LHA_IA98_%'