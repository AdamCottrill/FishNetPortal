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
def test_FN123_str():
    """Verify that the string representation of a FN123 object is the
    project code followed by sample number, effort, species code, and
    group code each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)

    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)

    shouldbe = "{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp)
    assert str(fn123) == shouldbe


@pytest.mark.django_db
def test_FN123_biocnt_on_save():
    """The FN123 object has a custom save method that update biocnt to
    reflect the current number of associated records in the
    FN125. This test verifies that it works as expected.

    """

    spc = 334
    species = SpeciesFactory(spc=spc)
    fn123 = FN123Factory(species=species)
    fn123.save()
    assert fn123.biocnt == 0

    fish = FN125Factory(catch=fn123)
    fish.save()
    fn123.save()

    assert fn123.biocnt == 1

    fish.delete()
    fn123.save()
    assert fn123.biocnt == 0
