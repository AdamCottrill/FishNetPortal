import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN124Factory,
    FN125Factory,
    FN127Factory,
)


@pytest.mark.django_db
def test_FN127_str():
    """Verify that the string representation of a FN127 object is the
    string reprentation of the associated fish, the assigned age and
    the ageid. The fish and ageid are separated by a dash, the age
    estimate is prefixed with age= and is wrapped in brackets.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (age=4)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    ageid = 12
    age = 8

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    fn127 = FN127Factory(fish=fn125, ageid=ageid, agea=age)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (age={})".format(
        project_code, sam, eff, spc, grp, fish_number, ageid, age
    )

    assert str(fn127) == shouldbe
