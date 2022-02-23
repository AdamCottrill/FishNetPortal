import pytest

from ..factories import (
    FN011Factory,
    FN013Factory,
)


@pytest.mark.django_db
def test_FN013_str():
    """Verify that the string representation of a FN013 object is the
    project the gear code, followed by the project code of the
    associated project.  The project code should be wrapped in
    brackets.

    """

    project_code = "LHA_IA00_123"
    gear_code = "GL99"

    project = FN011Factory(prj_cd=project_code)
    fn013 = FN013Factory(project=project, gr=gear_code)
    assert str(fn013) == "{} ({})".format(gear_code, project_code)
