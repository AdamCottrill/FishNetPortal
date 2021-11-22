"""=============================================================
~/fn_portal/tests/integraion_tests/ajax_views.py
 Created: 25 May 2020 15:38:05

 DESCRIPTION:

  there are a few views that do nothing but return data as a json
  resposne. These views are usually called from templates that are
  loaded by other views.  These could be replace by api views someday,
  but until then, lets make sure taht they returned exactly what we
  think they should.

 A. Cottrill
=============================================================

"""


import pytest
import json

from django.urls import reverse
from fn_portal.models import FN123
from ..fixtures import project


@pytest.mark.django_db
def test_project_catch_counts_json(client, project):
    """The project_catch_count_json view returns a json response that
    contains an item for every 123 record in the project. Each record
    contians the catch count and biocount, as well as spatio-temporal
    attributes of the net set.  Used mostly for project detail
    template map and graphs, but could be useful for some data
    analysis purposes.

    """

    url = reverse("fn_portal:project_catch_counts_json", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.content)

    # we should have 1 record for each fn123 record in our project
    expected_count = (
        FN123.objects.filter(effort__sample__project__slug=project.slug)
        .exclude(species__spc="000")
        .count()
    )
    assert len(data) == expected_count

    # the keys of the resposne should be:
    expected_keys = set(
        [
            "grp",
            "prj_cd",
            "sam",
            "eff",
            "lift_date",
            "dd_lat",
            "dd_lon",
            "gear",
            "effst",
            "sidep",
            "effdst",
            "grdep",
            "spc",
            "spc_code",
            "catch",
        ]
    )
    observed_keys = set(list(data[0].keys()))
    assert expected_keys == observed_keys

    # all of the species we caught should be in the dataset
    obs_species = set([x["spc_code"] for x in data])
    expected_species = set([x["spc"] for x in project.catch_counts()])
    assert obs_species == expected_species

    # there should not be any records for spc='000' or with catcnt=NULL
    assert "000" not in obs_species
    assert "0" not in obs_species


@pytest.mark.django_db
def test_sample_catch_counts_json(client, project):
    """The sample catch counts json view returns a json object that
    contains a single element for each species observed in this
    project.  It currently aggregrates across both eff and grp.

    """

    sample = project.samples.get(sam=1)

    url = reverse(
        "fn_portal:sample_catch_counts_json",
        kwargs={"slug": project.slug, "sam": sample.sam},
    )
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.content)

    # transform our queryset to match the json format that we are expecting:
    expected = [
        {"key": x["species"], "catcnt": x["catcnts"]} for x in sample.catch_counts()
    ]

    assert expected == data


@pytest.mark.django_db
def test_project_spc_biodata_json(client, project):
    """The project_species_biodata_json endpoint should return a json
    string that contains one item for each fish of the given speices
    caught in the given project. Each fish has both biological
    attributes as well as relevant details from the effort or net set
    (mesh size or water depth).  Used in FN_portal to populate the
    bioplots templates, but this api endpoint could also be very
    useful for data analysis purposes.

    """

    url = reverse(
        "fn_portal:project_spc_biodata_json", kwargs={"slug": project.slug, "spc": 334}
    )
    response = client.get(url)
    assert response.status_code == 200
    data = json.loads(response.content)

    # as our project has 6 walleye - three in eff1, 3 in effort 2:
    # project this will be true:
    assert len(data) == 6

    # the keys of the resposne should be:
    expected_keys = set(
        [
            "id",
            "sam",
            "grp",
            "lift_date",
            "yr",
            "sidep",
            "eff",
            "spc",
            "spc_nmco",
            "flen",
            "tlen",
            "rwt",
            "sex",
            "mat",
            "agea",
            "xagem",
            "clipc",
        ]
    )
    observed_keys = set(list(data[0].keys()))
    assert expected_keys == observed_keys
