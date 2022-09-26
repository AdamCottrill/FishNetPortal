"""
=============================================================
~/fn_portal/tests/api/crud_api/test_fn121.py
 Created: 08 Sep 2020 10:40:55

 DESCRIPTION:

  This file contains a number of unit tests that verify that the api
  endpoint for FN121 objects works as expected:

+ sample-list should be available to both logged in and anonomous users

+ sample-list be filterable for gear, site depth, date, grid(s)

+ sample detail should contains the proper elements:
   + "slug"
   + "sam"
   + "effdt0"
   + "effdt1"
   + "effdur"
   + "efftm0"
   + "efftm1"
   + "effst"
   + "sidep"
   + "site"
   + "grid5":
   + "dd_lat"
   + "dd_lon"
   + "sitem"
   + "comment1"
   + "secchi"


+ post, put and delete endpoint should only be available to admin or
project lead users, they should not be available for anaoous users, or
field crew (who cannot edit or create projects)

 A. Cottrill
=============================================================
"""


from datetime import datetime
from django.db.models.query import prefetch_related_objects

import pytest
from django.urls import reverse
from fn_portal.models import FN121
from rest_framework import status

from ..fixtures import api_client, grid, lake, net_sets, project, users


@pytest.fixture
def netset_data(grid):
    """A fixture that returns a dictionary corresponding to a net set object."""

    netset_data = {
        "sam": "16",
        "ssn": "00",
        "space": "11",
        "subspace": "00",
        "mode": "AA",
        "effdt0": "2019-10-03",
        "effdt1": "2019-10-04",
        "effdur": 25.00,
        "efftm0": "10:40:00",
        "efftm1": "11:40:00",
        "effst": "1",
        # "grtp": "GL",
        # "gr": "GL50",
        # "orient": "1",
        "sidep0": 5.7,
        "site": "44",
        "dd_lat0": 45.8595,
        "dd_lon0": -80.8095,
        # "grid5": {"grid": str(grid.grid), "slug": grid.slug},
        "grid5": str(grid.grid),
        "sitem0": 23,
        "comment1": "Some sample data",
        "secchi0": 10,
    }

    return netset_data


@pytest.mark.django_db
def test_fn121_listview(api_client, project, net_sets):
    """The FN121 list view should return a json resposne containing all of
    the net sets in a project.

    It should be available to any user.
    """

    prj_cd = project.prj_cd

    url = reverse("fn_portal_api:FN121_listview", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    data = [x.get("sam") for x in response.data["results"]]

    assert len(data) == 3

    expected = ["sam1", "sam2", "sam3"]
    for x in expected:
        assert x in data


@pytest.mark.django_db
def test_fn121_listview_none(api_client, project, net_sets):
    """If the list view is provided a project code that does not exist, it
    should return a 404 response and not throw an error.

    """
    # create a project code that does not exist:
    prj_cd = project.prj_cd[:-1] + "X"

    url = reverse("fn_portal_api:FN121_listview", kwargs={"prj_cd": prj_cd})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


# parameters for our list filter test.  Filter, value, and the expected
# sample numbers that should be returned.
filter_list = [
    ("active", "True", ["sam3"]),
    ("sidep__gte", "25", ["sam1", "sam3"]),
    ("sidep__lte", "25", ["sam2", "sam3"]),
    ("sidep0__gte", "25", ["sam1", "sam3"]),
    ("sidep0__lte", "25", ["sam2", "sam3"]),
    ("grtp", "TP", ["sam2"]),  # fail
    ("grtp", "TP,HP", ["sam2"]),  # fail
    ("grtp__not", "TP", ["sam1", "sam3"]),
    ("gr", "GL32", ["sam1"]),
    ("gr", "GL10,GL32", ["sam1", "sam3"]),
    ("gr__not", "GL32", ["sam2", "sam3"]),  # fail
    # # ("grid", "714", []),
    ("effdur__gte", "22.5", ["sam2"]),
    ("effdur__lte", "22.5", ["sam1"]),
    ("set_date", "2019-10-21", ["sam1"]),
    ("set_date__gte", "2019-10-21", ["sam1", "sam3"]),
    ("set_date__lte", "2019-10-21", ["sam1", "sam2"]),
    ("lift_date", "2019-10-22", ["sam1"]),
    ("lift_date__gte", "2019-10-22", ["sam1"]),
    ("lift_date__lte", "2019-10-22", ["sam1", "sam2"]),
    ("set_time", "12:00", ["sam3"]),
    ("set_time__gte", "12:00", ["sam2", "sam3"]),
    ("set_time__lte", "12:00", ["sam1", "sam3"]),
    ("lift_time", "13:30", ["sam2"]),
    ("lift_time__gte", "13:30", ["sam2"]),
    ("lift_time__lte", "13:30", ["sam1", "sam2"]),
]


@pytest.mark.parametrize("filter,value,expected", filter_list)
@pytest.mark.django_db
def test_fn121_listview_filters(api_client, project, net_sets, filter, value, expected):
    """The list view accepts filters for net set attributes as query
    parameters, these should limit the number net sets returned.

    this could be a parameterized query that accepts a filter, and a
    list of expected samples numbers that should be returned based on
    that filter.

    The list view end point has filters for a number of attribrutes:

    + active
    + sidep_gte
    + sidep_lte
    + grtp
    + gr
    + grid
    + effdur_gte
    + effdur_lte
    + set_date
    + set_date_gte
    + set_date_lte
    + lift_date
    + lift_date_gte
    + lift_date_lte
    + set_time
    + set_time_gte
    + set_time_lte
    + lift_time
    + lift_time_gte
    + lift_time_lte

    """
    q = "?{}={}".format(filter, value)
    url = reverse("fn_portal_api:FN121_listview", kwargs={"prj_cd": project.prj_cd})

    response = api_client.get(url + q)
    data = [x.get("sam") for x in response.data["results"]]
    for x in expected:
        assert x in data


username_list = [
    (None, status.HTTP_403_FORBIDDEN),
    ("gcostanza", status.HTTP_403_FORBIDDEN),
    ("hsimpson", status.HTTP_201_CREATED),
    ("bgumble", status.HTTP_201_CREATED),
    ("mburns", status.HTTP_201_CREATED),
]


@pytest.mark.parametrize("username,expected", username_list)
@pytest.mark.django_db
def test_fn121_listview_create_permissions(
    api_client, project, grid, netset_data, users, username, expected
):
    """a get request should be available for any user, a post request
    should only be available to authorized users.

    """

    if username:
        login = api_client.login(username=username, password="Abcd1234")
        assert login is True

    netset_data["project"] = project.prj_cd

    # ssn, space, and mode are slug related fields - repalce the
    # labels with the slugs so the serializer can create the relationships
    ssn = netset_data["ssn"]
    netset_data["ssn"] = f"{project.prj_cd}-{ssn}".lower()

    space = netset_data.pop("space")
    subspace = netset_data["subspace"]
    netset_data["subspace"] = f"{project.prj_cd}-{space}-{subspace}".lower()

    mode = netset_data["mode"]
    netset_data["mode"] = f"{project.prj_cd}-{mode}".lower()

    grid = netset_data["grid5"]
    netset_data["grid5"] = "hu_" + grid

    url = reverse("fn_portal_api:FN121_listview", kwargs={"prj_cd": project.prj_cd})
    response = api_client.post(url, netset_data, format="json")

    assert response.status_code == expected


@pytest.mark.django_db
def test_fn121_listview_create(api_client, project, grid, netset_data):
    """an authorized user should be able to create a new net set object by
    submitting an appropriate data object to the fn121 list view api
    endpoint.

    """

    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    netset_data["project"] = project.prj_cd

    # ssn, space, and mode are slug related fields - repalce the
    # labels with the slugs so the serializer can create the relationships
    ssn = netset_data["ssn"]
    netset_data["ssn"] = f"{project.prj_cd}-{ssn}".lower()

    space = netset_data.pop("space")
    subspace = netset_data["subspace"]
    netset_data["subspace"] = f"{project.prj_cd}-{space}-{subspace}".lower()

    mode = netset_data["mode"]
    netset_data["mode"] = f"{project.prj_cd}-{mode}".lower()

    grid = netset_data["grid5"]
    netset_data["grid5"] = "hu_" + grid

    url = reverse("fn_portal_api:FN121_listview", kwargs={"prj_cd": project.prj_cd})
    response = api_client.post(url, netset_data, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    # verify some of our attributes:
    fn121 = FN121.objects.get(project=project, sam=netset_data["sam"])

    assert fn121.effdt0 == datetime.strptime(netset_data["effdt0"], "%Y-%m-%d").date()
    assert fn121.effdt1 == datetime.strptime(netset_data["effdt1"], "%Y-%m-%d").date()
    assert fn121.effdur == netset_data["effdur"]
    assert fn121.efftm0 == datetime.strptime(netset_data["efftm0"], "%H:%M:%S").time()
    assert fn121.efftm1 == datetime.strptime(netset_data["efftm1"], "%H:%M:%S").time()
    assert fn121.effst == netset_data["effst"]

    assert fn121.sidep0 == netset_data["sidep0"]
    assert fn121.site == netset_data["site"]
    assert fn121.dd_lat0 == netset_data["dd_lat0"]
    assert fn121.dd_lon0 == netset_data["dd_lon0"]

    assert fn121.sitem0 == netset_data["sitem0"]
    assert fn121.comment1 == netset_data["comment1"]
    assert fn121.secchi0 == netset_data["secchi0"]

    grid = fn121.grid5
    assert grid.slug == netset_data["grid5"]


usernames = [None, "gcostanza", "hsimpson", "bgumble", "mburns"]


@pytest.mark.parametrize("username", usernames)
@pytest.mark.django_db
def test_fn121_detailview_get_permissions(
    api_client, project, net_sets, netset_data, username
):
    """a get request should be available to anyone."""

    net_set = net_sets[0]

    if username:
        login = api_client.login(username=username, password="Abcd1234")
        assert login is True

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})
    response = api_client.get(url)

    expected = status.HTTP_200_OK
    assert response.status_code == expected


@pytest.mark.django_db
def test_fn121_detailview(api_client, net_sets):
    """Ensure that the detail view includes all of the necessary elements
    and that that they correspond to the values in the net set.

    """

    net_set = net_sets[0]

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    expected = {
        "id": net_set.id,
        "slug": net_set.slug,
        "sam": net_set.sam,
        "ssn": net_set.ssn.ssn,
        "space": net_set.subspace.space.space,
        "subspace": net_set.subspace.subspace,
        "mode": net_set.mode.mode,
        "effdt0": net_set.effdt0.strftime("%Y-%m-%d"),
        "effdt1": net_set.effdt1.strftime("%Y-%m-%d"),
        "effdur": net_set.effdur,
        "efftm0": net_set.efftm0.strftime("%H:%M:%S"),
        "efftm1": net_set.efftm1.strftime("%H:%M:%S"),
        "effst": net_set.effst,
        "sidep0": net_set.sidep0,
        "site": net_set.site,
        # "grid5": {"grid": str(net_set.grid5.grid), "slug": net_set.grid5.slug},
        "grid5": str(net_set.grid5.grid),
        "dd_lat0": net_set.dd_lat0,
        "dd_lon0": net_set.dd_lon0,
        "sitem0": net_set.sitem0,
        "comment1": net_set.comment1,
        "secchi0": net_set.secchi0,
    }

    for k, v in expected.items():
        assert response.data[k] == v


@pytest.mark.parametrize("username", usernames)
@pytest.mark.django_db
def test_fn121_detailview_put_permissions(
    api_client, project, net_sets, netset_data, username
):
    """a put (update) request should only be available to authorized users."""

    net_set = net_sets[0]

    if username:
        login = api_client.login(username=username, password="Abcd1234")
        assert login is True

    netset_data["project"] = project.prj_cd
    # ssn, space, and mode are slug related fields - repalce the
    # labels with the slugs so the serializer can create the relationships
    ssn = netset_data["ssn"]
    netset_data["ssn"] = f"{project.prj_cd}-{ssn}".lower()

    space = netset_data.pop("space")
    subspace = netset_data["subspace"]

    netset_data["subspace"] = f"{project.prj_cd}-{space}-{subspace}".lower()

    mode = netset_data["mode"]
    netset_data["mode"] = f"{project.prj_cd}-{mode}".lower()

    grid = netset_data["grid5"]
    netset_data["grid5"] = "hu_" + grid

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})
    response = api_client.put(url, netset_data, format="json")

    if username is None or username == "gcostanza":
        expected = status.HTTP_403_FORBIDDEN
    else:
        expected = status.HTTP_200_OK
    assert response.status_code == expected


@pytest.mark.django_db
def test_fn121_update(api_client, project, net_sets):
    """An authorized user should be able update an object by sumbitting a
    put request to the FN121DetailView endpoint.

    """
    net_set = net_sets[0]
    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    new_data = {
        # "gr": "GL11",
        # "grtp": "GL",
        "effdt0": "2019-10-25",
        "effdt1": "2019-10-26",
        "efftm0": "09:30:00",
        "efftm1": "13:30:00",
        "effdur": 28.00,
    }

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})

    # get our original data:
    response = api_client.get(url, new_data, format="json")

    data = response.data.copy()
    for k, v in new_data.items():
        data[k] = v

    # we need to supply slugs for fk fields:
    prj_cd = project.prj_cd

    data["project"] = prj_cd
    # ssn, space, and mode are slug related fields - repalce the
    # labels with the slugs so the serializer can create the relationships
    ssn = data["ssn"]
    data["ssn"] = f"{prj_cd}-{ssn}".lower()

    space = data.pop("space")
    subspace = data["subspace"]
    data["subspace"] = f"{prj_cd}-{space}-{subspace}".lower()

    mode = data["mode"]
    data["mode"] = f"{prj_cd}-{mode}".lower()

    grid5 = data["grid5"]
    data["grid5"] = f"hu_{grid5}".lower()

    # now resubmit our updated data:
    response = api_client.put(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK

    # verify that our new values are reflected on our object:
    fn121 = FN121.objects.get(slug=net_set.slug)

    # check that the times are being converted propery too:
    assert fn121.effdt0 == datetime.strptime(new_data["effdt0"], "%Y-%m-%d").date()
    assert fn121.effdt1 == datetime.strptime(new_data["effdt1"], "%Y-%m-%d").date()
    assert fn121.effdur == new_data["effdur"]
    assert fn121.efftm0 == datetime.strptime(new_data["efftm0"], "%H:%M:%S").time()
    assert fn121.efftm1 == datetime.strptime(new_data["efftm1"], "%H:%M:%S").time()


@pytest.mark.parametrize("username", usernames)
@pytest.mark.django_db
def test_fn121_detailview_destroy_permissions(api_client, project, net_sets, username):
    """A delete request should only be available to authorized users."""

    net_set = net_sets[0]

    if username:
        login = api_client.login(username=username, password="Abcd1234")
        assert login is True

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})
    response = api_client.delete(url)

    if username is None or username == "gcostanza":
        expected = status.HTTP_403_FORBIDDEN
    else:
        expected = status.HTTP_204_NO_CONTENT
    assert response.status_code == expected


@pytest.mark.django_db
def test_fn121_destroy(api_client, project, net_sets):
    """An authorized user should be able to delete an object by sumbitting a
    delete request to the FN121DetailView endpoint.
    """

    net_set = net_sets[0]
    fn121 = FN121.objects.filter(project=project).count()
    assert fn121 == 3

    login = api_client.login(username="hsimpson", password="Abcd1234")
    assert login is True

    url = reverse("fn_portal_api:FN121_detailview", kwargs={"slug": net_set.slug})
    response = api_client.delete(url)

    expected = status.HTTP_204_NO_CONTENT
    assert response.status_code == expected

    fn121 = FN121.objects.filter(project=project).count()
    assert fn121 == 2
