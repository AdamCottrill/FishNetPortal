"""=============================================================
 ~/fn_portal/fn_portal/tests/api/test_FN012Readonly.py
 Created: 03 Jun 2021 11:31:56

 DESCRIPTION:

  The FN012 readonly endpoint should return a list of net sets.  The
  list of net sets accepts a large number of filters
  (url-parameters). Only net sets matching those criteria should be
  returned.

=============================================================

"""

import pytest
from django.urls import reverse
from rest_framework import status

from ...tests.fixtures import api_client

from ...tests.factories import (
    FN011Factory,
    FNProtocolFactory,
    LakeFactory,
    SpeciesFactory,
    FN012Factory,
    FN012ProtocolFactory,
)


@pytest.fixture
def project():
    """ """

    project = FN011Factory()
    species = SpeciesFactory(spc="091")

    FN012Factory(project=project, species=species)
    FN012Factory(project=project, species=species, grp="55", grp_des="the rest")

    return project


@pytest.fixture
def protocol():
    """ """

    protocol = FNProtocolFactory()
    lake = LakeFactory()
    species = SpeciesFactory(spc="091")

    FN012ProtocolFactory(protocol=protocol, lake=lake, species=species)
    FN012ProtocolFactory(
        protocol=protocol, lake=lake, species=species, grp="55", grp_des="the rest"
    )

    return protocol


@pytest.mark.django_db
def test_FN012_list(api_client, project):
    """when we access the readonly endpoint for FN012 objects, it should
    return a paginated list of sampling specs by species and group code.

    """

    url = reverse("fn_portal_api:sample_specs_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]

    assert len(payload) == 2

    expected = set([x.slug for x in project.sample_specs.all()])
    observed = set([x["slug"] for x in payload])
    assert expected == observed


@pytest.mark.django_db
def test_FN012Protocol_list(api_client, protocol):
    """when we access the readonly endpoint for FN012Protocol objects, it should
    return a paginated list of sampling specs by species and group code.

    """

    url = reverse("fn_portal_api:protocol_sample_specs_list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    payload = response.data["results"]

    assert len(payload) == 2

    expected = set([x.slug for x in protocol.sample_specs.all()])
    observed = set([x["slug"] for x in payload])
    assert expected == observed
