import pytest
from datetime import datetime

from ...models import FN022
from ...data_upload.upload_utils import (
    get_create_update_delete,
    create_update_delete,
    batch_update_model,
)
from ..factories import FN011Factory, FN022Factory


@pytest.fixture
def project():
    """ """

    prj_cd = "LHA_IA20_123"
    slug = prj_cd.lower()
    proj = FN011Factory(prj_cd=prj_cd, slug=slug)

    return proj


@pytest.fixture
def seasons(project):
    """ """

    slug = project.slug

    ssn = "01"
    ssn1 = FN022Factory(
        project=project,
        ssn=ssn,
        slug=f"{slug}-{ssn}",
        ssn_date0=datetime(2020, 1, 1),
        ssn_date1=datetime(2020, 1, 31),
    )

    ssn = "02"
    ssn2 = FN022Factory(
        project=project,
        ssn=ssn,
        slug=f"{slug}-{ssn}",
        ssn_date0=datetime(2020, 2, 1),
        ssn_date1=datetime(2020, 2, 28),
    )

    ssn = "03"
    ssn3 = FN022Factory(
        project=project,
        ssn=ssn,
        slug=f"{slug}-{ssn}",
        ssn_date0=datetime(2020, 3, 1),
        ssn_date1=datetime(2020, 3, 31),
    )

    return [ssn1, ssn2, ssn3]


@pytest.mark.django_db
def test_get_create_update_delete(project, seasons):
    """given a project with three seasons, and a dictionary of season
    data, get_create_update_delete should identify which seasons need to
    be created, deleted, or updated.

    """
    # ssn3 is gone, ssn9 is new
    data = [
        {"slug": f"{project.slug}-01"},
        {"slug": f"{project.slug}-02"},
        {"slug": f"{project.slug}-09"},
    ]

    filters = {
        "project__prj_cd__in": [
            project.prj_cd,
        ]
    }

    create_slugs, update_slugs, delete_slugs = get_create_update_delete(
        FN022, filters, data
    )

    expected = [
        f"{project.slug}-09",
    ]
    assert create_slugs == expected

    expected = [
        f"{project.slug}-01",
        f"{project.slug}-02",
    ]
    assert set(update_slugs) == set(expected)

    expected = [
        f"{project.slug}-03",
    ]
    assert delete_slugs == expected


@pytest.mark.django_db
def test_create_update_delete(project, seasons):
    """The create_update_delete() function should syncronyze the data in
    the database with the data passed in for the given model.  If we
    pass in a dictionary that is missing a season, has a new season,
    and one of the existing seasons has been updated, those changes
    should be reflected in the database after the function has run.

    """

    # ssn 1 is unchanged, ssn2 is updated, ssn3 is gone, ssn9 is new.

    data = [
        {
            "project_id": 1,
            "slug": f"{project.slug}-01",
            "ssn": "01",
            "ssn_date0": datetime(2020, 1, 1),
            "ssn_date1": datetime(2020, 1, 31),
        },
        {
            "project_id": 1,
            "slug": f"{project.slug}-02",
            "ssn": "02",
            "ssn_date0": datetime(2020, 2, 10),
            "ssn_date1": datetime(2020, 2, 15),
        },
        {
            "project_id": 1,
            "slug": f"{project.slug}-09",
            "ssn": "09",
            "ssn_date0": datetime(2020, 9, 1),
            "ssn_date1": datetime(2020, 9, 30),
        },
    ]

    filters = {
        "project__prj_cd__in": [
            project.prj_cd,
        ]
    }

    parent_map = {project.slug: project.id}
    parent_inverse = {1: project.slug}

    create_update_delete(data, FN022, filters, "project_id", parent_map, parent_inverse)

    ssns = project.seasons.all()
    slugs = [x.slug for x in ssns]
    expected = [
        f"{project.slug}-01",
        f"{project.slug}-02",
        f"{project.slug}-09",
    ]
    for slug in expected:
        assert slug in slugs

    assert f"{project.slug}-03" not in slugs

    # make sure that the dates have been updated too:
    ssn1 = project.seasons.get(ssn="01")
    # no change
    assert ssn1.ssn_date0 == datetime(2020, 1, 1).date()
    assert ssn1.ssn_date1 == datetime(2020, 1, 31).date()

    ssn2 = project.seasons.get(ssn="02")
    # updated
    assert ssn2.ssn_date0 == datetime(2020, 2, 10).date()
    assert ssn2.ssn_date1 == datetime(2020, 2, 15).date()

    ssn9 = project.seasons.get(ssn="09")
    # new
    assert ssn9.ssn_date0 == datetime(2020, 9, 1).date()
    assert ssn9.ssn_date1 == datetime(2020, 9, 30).date()


@pytest.mark.django_db
def test_batch_update_model(project, seasons):
    """the batch_update_model, function takes a django model a list list
    slugs that will be used to identify the model instances that need
    to be updated, and a list of dictionaries containing the updates.

    The attributes of the selected instance that differ from the
    dictionary should be updated, the other fields should remain
    unchanged.
    """

    pre_slugs = [x.slug for x in seasons]

    updates = {
        f"{project.slug}-01": {
            "slug": f"{project.slug}-01",
            "ssn": "01",
            "ssn_date0": datetime(2020, 1, 1),
            "ssn_date1": datetime(2020, 1, 31),
        },
        f"{project.slug}-02": {
            "slug": f"{project.slug}-02",
            "ssn": "02",
            "ssn_date0": datetime(2020, 2, 10),
            "ssn_date1": datetime(2020, 2, 15),
        },
    }

    update_slugs = list(updates.keys())

    batch_update_model(FN022, update_slugs, updates)

    post_slugs = [x.slug for x in project.seasons.all()]
    assert set(pre_slugs) == set(post_slugs)

    # make sure that the dates have been updated too:
    ssn1 = project.seasons.get(ssn="01")
    # no change
    assert ssn1.ssn_date0 == datetime(2020, 1, 1).date()
    assert ssn1.ssn_date1 == datetime(2020, 1, 31).date()

    ssn2 = project.seasons.get(ssn="02")
    # updated
    assert ssn2.ssn_date0 == datetime(2020, 2, 10).date()
    assert ssn2.ssn_date1 == datetime(2020, 2, 15).date()

    ssn3 = project.seasons.get(ssn="03")
    # not included in updates, should be unchanged
    assert ssn3.ssn_date0 == datetime(2020, 3, 1).date()
    assert ssn3.ssn_date1 == datetime(2020, 3, 31).date()
