import pytest

from ..factories import (
    FN011Factory,
    FN013Factory,
    FN014Factory,
)


@pytest.mark.django_db
def test_FN014_str():
    """Verify that the string representation of a FN014 object is the gear
    code, followed by the effort (mesh size), folled by the project code
    of the associated project.  The gear code and mesh size are
    separted by a dash, while the project code should be wrapped in
    brackets.

    """

    project_code = "LHA_IA00_123"
    gear_code = "GL99"
    effort = "99"

    project = FN011Factory(prj_cd=project_code)
    fn013 = FN013Factory(project=project, gr=gear_code)
    fn014 = FN014Factory(gear=fn013, eff=effort)

    assert str(fn014) == "{}-{} ({})".format(gear_code, effort, project_code)
