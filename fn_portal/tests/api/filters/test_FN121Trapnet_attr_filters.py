import pytest
from django.urls import reverse
from rest_framework import status

from ...factories import (
    FN011Factory,
    FN121Factory,
    FN121TrapnetFactory,
    BottomTypeFactory,
    CoverTypeFactory,
)


# precip0 an precip1
# wind_direction0 and wind_direction1
# cloud_pc0 an cloud_pc1
# wave_duration
# waveht_duration


@pytest.fixture
def trapnet_data():
    """create several sets of with known attributes and return them in an
    array"""

    bottom1 = BottomTypeFactory(abbrev="BR", label="Bedrock or Rock")
    bottom2 = BottomTypeFactory(abbrev="CL", label="Clay")
    bottom3 = BottomTypeFactory(abbrev="DE", label="Detritus")
    bottom4 = BottomTypeFactory(abbrev="MA", label="Marl")

    cover1 = CoverTypeFactory(abbrev="CO", label="Combination")
    cover2 = CoverTypeFactory(abbrev="LT", label="Log & Tree")
    cover3 = CoverTypeFactory(abbrev="MA", label="Macrophytes")
    cover4 = CoverTypeFactory(abbrev="NC", label="No Cover")

    project = FN011Factory()
    sample1 = FN121Factory(project=project)
    trapnet1 = FN121TrapnetFactory(
        sample=sample1,
        leaduse=8.1,
        lead_angle=90,
        distoff=None,
        bottom=bottom1,
        cover=None,
    )

    sample2 = FN121Factory(project=project)
    trapnet2 = FN121TrapnetFactory(
        sample=sample2,
        leaduse=10,
        lead_angle=90,
        distoff=2,
        bottom=bottom3,
        cover=None,
    )

    sample3 = FN121Factory(project=project)
    trapnet3 = FN121TrapnetFactory(
        sample=sample3,
        leaduse=None,
        lead_angle=30,
        distoff=2,
        bottom=bottom2,
        cover=cover4,
    )

    sample4 = FN121Factory(project=project)
    trapnet4 = FN121TrapnetFactory(
        sample=sample4,
        leaduse=13,
        lead_angle=60,
        distoff=5,
        bottom=None,
        cover=cover3,
    )

    sample5 = FN121Factory(project=project)
    trapnet5 = FN121TrapnetFactory(
        sample=sample5,
        leaduse=20,
        lead_angle=None,
        distoff=0,
        bottom=None,
        cover=cover2,
    )

    sample6 = FN121Factory(project=project)
    trapnet6 = FN121TrapnetFactory(
        sample=sample6,
        leaduse=8.1,
        lead_angle=None,
        distoff=1,
        bottom=bottom4,
        cover=cover1,
    )

    return [trapnet1, trapnet2, trapnet3, trapnet4, trapnet5, trapnet6]


filter_args = [
    ({"leaduse": 10}, [1]),
    ({"leaduse__gte": 10}, [1, 3, 4]),
    ({"leaduse__lte": 10}, [0, 1, 5]),
    ({"leaduse__gt": 10}, [3, 4]),
    ({"leaduse__lt": 10}, [0, 5]),
    ({"leaduse__null": "true"}, [2]),
    ({"leaduse__null": "false"}, [0, 1, 3, 4, 5]),
    ({"leaduse__not_null": "true"}, [0, 1, 3, 4, 5]),
    (
        {"leaduse__not_null": "false"},
        [
            2,
        ],
    ),
    ({"lead_angle": 60}, [3]),
    ({"lead_angle__gte": 60}, [0, 1, 3]),
    ({"lead_angle__lte": 60}, [2, 3]),
    ({"lead_angle__gt": 60}, [0, 1]),
    (
        {"lead_angle__lt": 60},
        [
            2,
        ],
    ),
    ({"lead_angle__null": "true"}, [4, 5]),
    (
        {"lead_angle__null": "false"},
        [
            0,
            1,
            2,
            3,
        ],
    ),
    (
        {"lead_angle__not_null": "true"},
        [
            0,
            1,
            2,
            3,
        ],
    ),
    ({"lead_angle__not_null": "false"}, [4, 5]),
    ({"distoff": 2}, [1, 2]),
    ({"distoff__gte": 2}, [1, 2, 3]),
    ({"distoff__lte": 2}, [1, 2, 4, 5]),
    ({"distoff__gt": 2}, [3]),
    ({"distoff__lt": 2}, [4, 5]),
    ({"distoff__null": "true"}, [0]),
    ({"distoff__null": "false"}, [1, 2, 3, 4, 5]),
    ({"distoff__not_null": "true"}, [1, 2, 3, 4, 5]),
    (
        {"distoff__not_null": "false"},
        [
            0,
        ],
    ),
    ({"bottom_type": "BR"}, [0]),
    ({"bottom_type": "BR, CL"}, [0, 2]),
    ({"bottom_type__not": "BR, CL"}, [1, 3, 4, 5]),
    ({"bottom_type__null": "true"}, [3, 4]),
    ({"bottom_type__null": "false"}, [0, 1, 2, 5]),
    ({"cover_type": "CO"}, [5]),
    ({"cover_type": "CO, LT"}, [4, 5]),
    ({"cover_type__not": "CO, LT"}, [0, 1, 2, 3]),
    ({"cover_type__null": "true"}, [0, 1]),
    ({"cover_type__null": "false"}, [2, 3, 4, 5]),
]


@pytest.mark.django_db
@pytest.mark.parametrize("filter,expected", filter_args)
def test_FN121TrapnetReadonly_filters(client, trapnet_data, filter, expected):
    """The readonly api endpoint for FN121Trapnet objects accepts a large number
    filters that are associated with attributes of the FN121Trapnet table.

    This test is parameterized to accept a list of two element tuples, the
    filter is the filter to apply, the second is the list of indices that
    correspond to the FN121Trapnet records that should be returned in the response.
    The indices are used to extract the slugs from the fixture and compare those
    to the slugs returned by the response.

    """

    slugs = []
    for i, x in enumerate(trapnet_data):
        if i in expected:
            slugs.append(x.slug)

    url = reverse("fn_portal_api:fn121trapnet_list")
    response = client.get(url, filter)
    assert response.status_code == status.HTTP_200_OK

    # pull out the slugs from the response:
    payload = response.data["results"]
    observed_slugs = {x["slug"] for x in payload}

    assert len(payload) == len(expected)
    assert set(slugs) == observed_slugs
