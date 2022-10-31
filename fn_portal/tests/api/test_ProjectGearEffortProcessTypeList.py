"""This test file verifies that the project specific
  gear-effort-process type endpoint returns the correct values as
  specified for the project.  It includes test setup fixture, a list
  of expected results, and a parameterized function that verifies the
  response contains the exected ressults.

  Here is a summary of bhe basic project setup:

  + LHA_IA20_AAA -> one gear, one process types
  + LHA_IA20_BBB -> one gear two process types
  + LHA_IA20_CCC -> two gears, one process type each
  + LHA_IA20_DDD -> two gears, two process types

"""

import pytest
from django.urls import reverse
from rest_framework import status

from ..factories import (
    FN011Factory,
    GearEffortProcessTypeFactory,
    GearFactory,
    ProjectGearProcessTypeFactory,
)
from ..fixtures import api_client


@pytest.fixture
def projects():
    """Our tests will require a couple of gears, with different
    process types and a couple of different projects to ensure the api
    endpoint returns the expected values.

    """

    gl50 = GearFactory(gr_code="GL50", grtp="GL")
    gl10 = GearFactory(gr_code="GL10", grtp="GL")

    # gear effort process types:
    GearEffortProcessTypeFactory(gear=gl50, eff="000", effdst=500, process_type="1")
    GearEffortProcessTypeFactory(gear=gl50, eff="001", effdst=250, process_type="2")
    GearEffortProcessTypeFactory(gear=gl50, eff="002", effdst=250, process_type="2")
    GearEffortProcessTypeFactory(gear=gl10, eff="000", effdst=200, process_type="1")
    GearEffortProcessTypeFactory(gear=gl10, eff="001", effdst=100, process_type="2")
    GearEffortProcessTypeFactory(gear=gl10, eff="002", effdst=100, process_type="2")

    # one gear, one process types
    projectA = FN011Factory(prj_cd="LHA_IA20_AAA")
    ProjectGearProcessTypeFactory(project=projectA, gear=gl50, process_type="1")

    # one gear two process types
    projectB = FN011Factory(prj_cd="LHA_IA20_BBB")
    ProjectGearProcessTypeFactory(project=projectB, gear=gl50, process_type="1")
    ProjectGearProcessTypeFactory(project=projectB, gear=gl50, process_type="2")

    # two gears, one process type each
    projectC = FN011Factory(prj_cd="LHA_IA20_CCC")
    ProjectGearProcessTypeFactory(project=projectC, gear=gl50, process_type="1")
    ProjectGearProcessTypeFactory(project=projectC, gear=gl10, process_type="1")

    # two gears, two process types
    projectD = FN011Factory(prj_cd="LHA_IA20_DDD")
    ProjectGearProcessTypeFactory(project=projectD, gear=gl50, process_type="1")
    ProjectGearProcessTypeFactory(project=projectD, gear=gl50, process_type="2")
    ProjectGearProcessTypeFactory(project=projectD, gear=gl10, process_type="1")
    ProjectGearProcessTypeFactory(project=projectD, gear=gl10, process_type="2")

    return [projectA, projectB, projectC, projectD]


expected_values_list = [
    (
        "LHA_IA20_AAA",
        [
            {"gr": "GL50", "process_type": "1", "eff": "000", "effdst": 500},
        ],
    ),
    (
        "LHA_IA20_BBB",
        [
            {"gr": "GL50", "process_type": "1", "eff": "000", "effdst": 500},
            {"gr": "GL50", "process_type": "2", "eff": "001", "effdst": 250},
            {"gr": "GL50", "process_type": "2", "eff": "002", "effdst": 250},
        ],
    ),
    (
        "LHA_IA20_CCC",
        [
            {"gr": "GL50", "process_type": "1", "eff": "000", "effdst": 500},
            {"gr": "GL10", "process_type": "1", "eff": "000", "effdst": 200},
        ],
    ),
    (
        "LHA_IA20_DDD",
        [
            {"gr": "GL50", "process_type": "1", "eff": "000", "effdst": 500},
            {"gr": "GL50", "process_type": "2", "eff": "001", "effdst": 250},
            {"gr": "GL50", "process_type": "2", "eff": "002", "effdst": 250},
            {"gr": "GL10", "process_type": "1", "eff": "000", "effdst": 200},
            {"gr": "GL10", "process_type": "2", "eff": "001", "effdst": 100},
            {"gr": "GL10", "process_type": "2", "eff": "002", "effdst": 100},
        ],
    ),
]


@pytest.mark.django_db
@pytest.mark.parametrize("prj_cd,expected", expected_values_list)
def test_project_gear_effort_process_type_list(api_client, projects, prj_cd, expected):
    """The ProjectGearEffortProcessTypeList endpoint should return a
    list of the gears, process types, and efforts for each gear type
    associated with a single project.

    this is a parametersized query that accepts a project code and
    verifies that the returned gear effort process types match the
    expected values established in the setup ficture (projects)


    # LHA_IA20_AAA -> one gear, one process types
    # LHA_IA20_BBB -> one gear two process types
    # LHA_IA20_CCC -> two gears, one process type each
    # LHA_IA20_DDD -> two gears, two process types


    """
    kwargs = {"slug": prj_cd.lower()}
    url = reverse("fn_portal_api:project_gear_eff_process_types", kwargs=kwargs)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    for val in expected:
        assert val in response.data
