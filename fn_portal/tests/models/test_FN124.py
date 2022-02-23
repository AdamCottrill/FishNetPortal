import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN124Factory,
)


@pytest.mark.django_db
def test_FN124_str():
    """
    Verify that the string representation of a FN124 object is the
    project code followed by sample number, effort, species code,
    group code and size calss each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00-350

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    siz = 350

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn124 = FN124Factory(catch=fn123, siz=siz)

    shouldbe = "{}-{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp, siz)
    assert str(fn124) == shouldbe
