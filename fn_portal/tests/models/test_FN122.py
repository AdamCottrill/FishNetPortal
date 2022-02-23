import pytest

from ..factories import (
    FN011Factory,
    FN121Factory,
    FN122Factory,
)


@pytest.mark.django_db
def test_FN122_str():
    """
    Verify that the string representation of a FN122 object is the project
    code followed by sample number and effort each separated by a dash.

    e.g. - LHA_IA00_123-001-051

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    shouldbe = "{}-{}-{}".format(project_code, sam, eff)
    assert str(fn122) == shouldbe
