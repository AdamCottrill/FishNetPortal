import pytest

from ..factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
    FN125TagFactory,
)


@pytest.mark.django_db
def test_FN125Tags_str():
    """Verify that the string representation of a FN_Tags object is the
    string reprentation of the associated fish, the tag number and the
    tag documentation string. The fish and tag number are separated by
    a dash, the tagdoc string is wrapped in brackets.

    e.g. - LHA_IA00_123-001-051-091-00-1-65984 (25012)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    fish_tag_id = 11
    tagnumber = 78910
    tagdoc = 12345

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    tag = FN125TagFactory(
        fish=fn125, fish_tag_id=fish_tag_id, tagid=tagnumber, tagdoc=tagdoc
    )

    shouldbe = "{}-{}-{}-{}-{}-{}-{} ({} ({}))".format(
        project_code, sam, eff, spc, grp, fish_number, fish_tag_id, tagnumber, tagdoc
    )

    assert str(tag) == shouldbe
