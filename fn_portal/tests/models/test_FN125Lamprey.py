import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
    FN125LampreyFactory,
)


@pytest.mark.django_db
def test_FN125Lamprey_xlam_str():
    """Verify that the string representation of a lamprey wound object is the
    string reprentation of the associated fish, the wound number and the
    xlam string.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (xlam: 0101)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    lamid = 11
    xlam = "0101"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    lamprey = FN125LampreyFactory(fish=fn125, lamid=lamid, xlam=xlam)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (xlam: {})".format(
        project_code, sam, eff, spc, grp, fish_number, lamid, xlam
    )

    assert str(lamprey) == shouldbe


@pytest.mark.django_db
def test_FN125Lamprey_lamijc_str():
    """Verify that the string representation of a lamprey wound object is the
    string reprentation of the associated fish, the wound number and the
    lamijc string.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (lamijc: A235)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    lamid = 11
    lamijc_type = "A1"
    lamijc_size = "25"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    lamprey = FN125LampreyFactory(
        fish=fn125, lamid=lamid, lamijc_size=lamijc_size, lamijc_type=lamijc_type
    )

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (lamijc: {}{})".format(
        project_code, sam, eff, spc, grp, fish_number, lamid, lamijc_type, lamijc_size
    )

    assert str(lamprey) == shouldbe
