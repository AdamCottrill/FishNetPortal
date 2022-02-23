import pytest

from ..factories import FN011Factory, FN121Factory


@pytest.mark.django_db
def test_FN121_str():
    """
    Verify that the string representation of a FN121 object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    shouldbe = "{}-{}".format(project_code, sam)
    assert str(fn121) == shouldbe


@pytest.mark.xfail
def test_switched_dates():
    """If the lift date occurs before the set date and error
    should be thrown."""
    assert 0 == 1


@pytest.mark.xfail
def test_dates_of_bounds():
    """The set or lift date is outside of the dates associated with the
    season, an error should be raised.

    """
    assert 0 == 1
