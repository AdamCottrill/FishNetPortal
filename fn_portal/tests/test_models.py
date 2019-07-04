import pytest

from .factories import FN011Factory


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
