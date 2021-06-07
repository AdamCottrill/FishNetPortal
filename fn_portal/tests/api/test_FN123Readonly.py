"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN123Readonly.py
 Created: 07 Jun 2021 13:56:02

 DESCRIPTION:

  The FN123 readonly endpoint should return a list of efforts.  The
  list of efforts accepts a large number of filters (url-parameters)
  assocaited with the effort, or attributes of the net and
  project. Only efforts matching those criteria should be returned
  when query parameters are provided.


=============================================================

"""

import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client
from ...tests.factories import (
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    SpeciesFactory,
)


@pytest.fixture
def fn123_records():

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    eff1 = FN122Factory(sample=fn121, eff="001")

    spc = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )

    catch1 = FN123Factory(effort=eff1, species=spc, grp="55")
    catch2 = FN123Factory(effort=eff1, species=spc, grp="11")
    return [catch1, catch2]


@pytest.mark.django_db
def test_FN123Readonly_list(api_client, fn123_records):
    """when we access the readonly endpoint for FN123 objects, it should
    return a paginated list of efforts that includes all of the FN123
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:catchcount_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn123 in fn123_records:
        assert fn123.slug in observed


def test_FN123Readonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN123 readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:catchcount_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.xfail
def test_FN123Readonly_filters():
    """The readonly api endpoint for FN123 objects accepts a large number
    of potential parameters as filters. This test will verify that only
    catch counts matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN123 slugs expected in the
    response.

    """
    assert 0 == 1
