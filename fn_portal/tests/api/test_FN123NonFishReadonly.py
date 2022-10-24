"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN123NonFishReadonly.py
 Created: 20 Oct 2022 17:25:23


 DESCRIPTION:

  The FN123NonFish readonly endpoint should return a list of efforts.  The
  list of efforts accepts a large number of filters (url-parameters)
  assocaited with the effort, or attributes of the net and
  project. Only efforts matching those criteria should be returned
  when query parameters are provided.


=============================================================

"""

from django.core.validators import int_list_validator
import pytest

from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client, taxon_list
from ...tests.factories import (
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123NonFishFactory,
    TaxonFactory,
)


@pytest.fixture
def fn123nonfish_records(taxon_list):
    """Set up a project with a net that caught the same taxon in two
    different efforts."""

    fn011 = FN011Factory(prj_cd="LHA_IA10_123")
    fn121 = FN121Factory(project=fn011, sam=1)

    eff1 = FN122Factory(sample=fn121, eff="001")

    # itis code for a taxon in taxon_list:
    taxon1 = TaxonFactory(itiscode=161989)
    taxon2 = TaxonFactory(itiscode=162002)

    catch1 = FN123NonFishFactory(effort=eff1, taxon=taxon1)
    catch2 = FN123NonFishFactory(effort=eff1, taxon=taxon2)
    return [catch1, catch2]


@pytest.mark.django_db
def test_FN123NonFishReadonly_list(api_client, fn123nonfish_records):
    """when we access the readonly endpoint for FN123NonFish objects, it should
    return a paginated list of efforts that includes all of the FN123NonFish
    objects in the database (ie. un-filtered).

    """

    url = reverse("fn_portal_api:FN123NonFish_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    observed = set([x["slug"] for x in payload])
    for fn123 in fn123nonfish_records:
        assert fn123.slug in observed


@pytest.mark.django_db
def test_FN123NonFishReadonly_only_get_allowed(api_client, fn123nonfish_records):
    """Only get requests are allowed on the FN123NonFish readonly endpoint.  This
    test verifies taht other methods are denied.

    """

    url = reverse("fn_portal_api:FN123NonFish_list")
    response = api_client.post(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.put(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.patch(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN

    response = api_client.delete(url, data={})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_FN121WeatherReadonly_expected_keys(api_client, fn123nonfish_records):
    """Verify that the FN121Weather objects returned by the list view have
    the expected keys.  Especially those that will allow it to be joined
    back up to the parent net set and project.
    """

    url = reverse("fn_portal_api:FN123NonFish_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    assert len(payload) == 2

    # get the keys from the first object and verify that they match
    # what we expect (at a minimum, we should expect slug, prj_cd and
    # sam will be included in the response:
    observed = payload[0].keys()
    expected = [
        "prj_cd",
        "sam",
        "eff",
        "taxon",
        "catcnt",
        "mortcnt",
        "comment3",
        "slug",
        "id",
    ]

    assert set(observed) == set(expected)


taxon_node_list = [
    # rainbow trout - same as one taxon
    (
        161989,
        [
            "161989",
        ],
    ),
    # Salvelinus - parent of one taxon
    (
        161999,
        [
            "162002",
        ],
    ),
    # Salmonidae - parent of both taxon:
    (623286, ["162002", "161989"]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("tsn,expected", taxon_node_list)
def test_FN123NonFishReadonly_taxon_node_filters(
    api_client, fn123nonfish_records, tsn, expected
):
    """The readonly api endpoint for FN123NonFish objects accepts a
    special filter taxon_node that accepts a taxon code and returns
    only those records in that node ot below - allows us to get all of
    the turtles without know what species was reported.

    """

    url = reverse("fn_portal_api:FN123NonFish_list")
    response = api_client.get(url, {"taxon_node": tsn})
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]
    observed = set([x["taxon"] for x in payload])
    assert set(expected) == observed


@pytest.mark.xfail
def test_FN123NonFishReadonly_filters():
    """The readonly api endpoint for FN123NonFish objects accepts a large number
    of potential parameters as filters. This test will verify that only
    catch counts matcing the specified criteria are returned.

    This test will be parameterized with a list of two element tuples,
    the filter to apply, and a list of the FN123NonFish slugs expected in the
    response.

    """
    assert 0 == 1
