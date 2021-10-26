"""=============================================================
~/fn_portal/tests/api/fixtures.py
 Created: 08 Apr 2020 10:46:00

 DESCRIPTION:

  A number of fixtures that will be used in testing the api endpoints
  for fn_portal


=============================================================

"""


from datetime import datetime, time

import pytest
from fn_portal.tests.factories.FN0_factories import (
    FN022Factory,
    FN026Factory,
    FN028Factory,
)

from ..factories import (
    FN011Factory,
    FN121Factory,
    GearFactory,
    Grid5Factory,
    LakeFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def users():
    """Create some users that will be project leads, feild crew,
    super-users/administrators, and regular employees."""

    user0 = UserFactory(username="hsimpson")
    user0.set_password("Abcd1234")
    user0.save()

    user1 = UserFactory(username="bgumble")
    user1.set_password("Abcd1234")
    user1.save()

    user2 = UserFactory(username="gcostanza")
    user2.set_password("Abcd1234")
    user2.save()

    user3 = UserFactory(username="mburns")
    user3.set_password("Abcd1234")
    user3.is_staff = True
    user3.is_admin = True
    user3.save()

    return [user0, user1, user2, user3]


@pytest.fixture
def project(users):

    # homer and barney will be associated with this project:
    user = users[0]
    user1 = users[1]

    project1 = FN011Factory(
        prj_ldr=user,
        prj_cd="LHA_IA19_001",
        prj_date0=datetime(2019, 10, 1),
        prj_date1=datetime(2019, 11, 1),
        prj_nm="First Project",
    )
    project1.field_crew.add(user1)
    project1.save()

    FN022Factory(ssn="00", project=project1, __sequence=1)

    FN026Factory(project=project1, space="11", space_des="a test space", __sequence=1)

    gl32 = GearFactory(gr_code="GL32", grtp="GL")
    FN028Factory(mode="AA", project=project1, gear=gl32, __sequence=1)

    return project1


@pytest.fixture
def lake():
    """"""
    lake = LakeFactory(lake_name="Lake Huron", abbrev="HU")
    return lake


@pytest.fixture
def grid(lake):
    """"""
    grid = Grid5Factory(lake=lake, grid=1234)
    return grid


@pytest.fixture
def ssn(project):
    """"""
    ssn = FN022Factory(project=project, ssn="00", ssn_des="a test ssn", __sequence=1)
    return ssn


@pytest.fixture
def space(project):
    """"""
    space = FN026Factory(
        project=project, space="11", space_des="a test space", __sequence=1
    )
    return space


@pytest.fixture
def mode(project, gear):
    """"""
    mode = FN028Factory(project=project, gear=gear, __sequence=1)
    return mode


@pytest.fixture
def net_sets(project, grid):
    gl32 = GearFactory(gr_code="GL32", grtp="GL")
    mode1 = FN028Factory(project=project, gear=gl32, __sequence=1)

    tp02 = GearFactory(gr_code="TP02", grtp="TP")
    mode2 = FN028Factory(project=project, gear=tp02)

    gl10 = GearFactory(gr_code="GL10", grtp="GL")
    mode3 = FN028Factory(project=project, gear=gl10)

    ssn = FN022Factory(ssn="00", project=project, __sequence=1)
    space = FN026Factory(
        project=project, space="11", space_des="a test space", __sequence=1
    )

    sam1 = FN121Factory(
        mode=mode1,
        project=project,
        sam="sam1",
        ssn=ssn,
        space=space,
        effdt0=datetime(2019, 10, 21),
        effdt1=datetime(2019, 10, 22),
        efftm0=time(10, 30),
        efftm1=time(8, 30),
        effdur=22.0,
        grid5=grid,
        sidep=40,
    )
    sam2 = FN121Factory(
        mode=mode2,
        project=project,
        sam="sam2",
        ssn=ssn,
        space=space,
        grid5=grid,
        effdt0=datetime(2019, 10, 20),
        effdt1=datetime(2019, 10, 21),
        efftm0=time(12, 0),
        efftm1=time(13, 30),
        effdur=25.5,
        sidep=10,
    )
    sam3 = FN121Factory(
        mode=mode3,
        project=project,
        sam="sam3",
        ssn=ssn,
        space=space,
        grid5=grid,
        effdt0=datetime(2019, 10, 22),
        efftm0=time(12, 0),
        sidep=25,
    )

    return [sam1, sam2, sam3]
