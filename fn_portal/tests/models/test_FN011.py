import pytest

from ..factories import FN011Factory


@pytest.mark.django_db
def test_FN011_str():
    """
    Verify that the string representation of a FN011 object is the project
    name followed by the project code in brackets.
    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name)
    assert str(obj) == "{} ({})".format(project_name, project_code)


year_values = [None, ""]


@pytest.mark.django_db
@pytest.mark.parametrize("year", year_values)
def test_FN011_year_on_save(year):
    """The Fn011 model has a custom save function that creates the slug
    and populates the year if it is null or an empty string.  Verify that it works.

    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name, year=year)
    assert obj.year == "2000"


@pytest.mark.django_db
def test_FN011_slug_on_save():
    """The Fn011 model has a custom save function that creates the slug
    from the project code

    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name)
    assert obj.slug == project_code.lower()


@pytest.mark.xfail
def test_year_inconsistent_with_prj_cd():
    """If the year associated with the project is not consistent with the
    project code and error should be thrown.

    """
    assert 0 == 1


@pytest.mark.xfail
def test_dates_inconsistent_with_prj_cd():
    """If the start and/or end date of the project are not consistent with
    the project code and error should be thrown.

    This test should be parameterized.

    """
    assert 0 == 1
