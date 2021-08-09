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

from ..factories import (
    FN011Factory,
    FN121Factory,
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

    project1 = FN011Factory(prj_ldr=user, prj_cd="LHA_IA19_001", prj_nm="First Project")
    project1.field_crew.add(user1)
    project1.save()

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
def net_sets(project, grid):

    sam1 = FN121Factory(
        project=project,
        sam="sam1",
        effdt0=datetime(2019, 10, 21),
        effdt1=datetime(2019, 10, 22),
        efftm0=time(10, 30),
        efftm1=time(8, 30),
        effdur=22.0,
        grid5=grid,
        sidep=40,
        gr="GL32",
        grtp="GL",
    )
    sam2 = FN121Factory(
        project=project,
        sam="sam2",
        effdt0=datetime(2019, 10, 20),
        effdt1=datetime(2019, 10, 21),
        efftm0=time(12, 0),
        efftm1=time(13, 30),
        effdur=25.5,
        sidep=10,
        gr="TP02",
        grtp="TP",
    )
    sam3 = FN121Factory(
        project=project,
        sam="sam3",
        effdt0=datetime(2019, 10, 22),
        # effdt1=datetime(2019, 10, 23),
        efftm0=time(12, 0),
        # efftm1=time(12, 30),
        sidep=25,
        gr="GL10",
        grtp="GL",
    )

    return [sam1, sam2, sam3]
