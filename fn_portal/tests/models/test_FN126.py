import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN124Factory,
    FN125Factory,
    FN126Factory,
)


@pytest.mark.django_db
def test_FN126_str():
    """Verify that the string representation of a field collected diet
    item is the string reprentation of the associated
    fish, the food id, the taxon, and foodcount (in brackets)

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (F121: 3)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    food = 1
    taxon = "F121"
    fdcnt = 8

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    fn126 = FN126Factory(fish=fn125, food=food, taxon=taxon, fdcnt=fdcnt)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} ({}: {})".format(
        project_code, sam, eff, spc, grp, fish_number, food, taxon, fdcnt
    )

    assert str(fn126) == shouldbe
