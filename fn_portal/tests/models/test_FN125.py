import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
)


@pytest.mark.django_db
def test_FN125_str():
    """
    Verify that the string representation of a FN125 object is the
    project code followed by sample number, effort, species code,
    group code and fish number each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00-1

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)

    shouldbe = "{}-{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp, fish_number)
    assert str(fn125) == shouldbe
