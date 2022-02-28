"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN121Readonly.py
 Created: 03 Jun 2021 11:31:56

 DESCRIPTION:

  The FN121 readonly endpoint should return a list of net sets.  The
  list of net sets accepts a large number of filters
  (url-parameters). Only net sets matching those criteria should be
  returned.

=============================================================

"""

import pytest
from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client, project


@pytest.mark.django_db
def test_FN121Readonly_list(api_client, project):
    """when we access the readonly endpoint for FN121 objects, it should
    return a paginated list of net sets that includes all of the FN121
    objects in the database (ie. unfiltered).

    """

    url = reverse("fn_portal_api:netset_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]

    assert len(payload) == 2

    expected = set([x.slug for x in project.samples.all()])
    observed = set([x["slug"] for x in payload])
    assert expected == observed


def test_FN121Readonly_only_get_allowed(api_client):
    """Only get requests are allowed on the FN121 readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:netset_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.xfail
def test_FN121Readonly_filters():
    """The readonly api endpoint for FN121 objects accepts a large number
    of potential parameters as filters. This test will verify that only
    net sets matching the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN121 slugs expected in the
    response.

    """
    assert 0 == 1
