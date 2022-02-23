import pytest
from datetime import datetime
from django.db import IntegrityError


from fn_portal.models import FN022
from ..factories import FN011Factory, FN022Factory


@pytest.mark.django_db
def test_FN022_str():
    """Verify that a sesaon is represented by object type, season description,
    season code, project code and for the associated project."""

    ssn = "11"
    ssn_des = "Early Summer"
    prj_cd = "LHA_IA11_123"

    project = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(project=project, ssn=ssn, ssn_des=ssn_des)

    shouldbe = "<Season: {} ({}) [{}]>".format(ssn_des, ssn, prj_cd)

    assert str(season) == shouldbe


@pytest.mark.django_db()
def test_duplicate_season():
    """The season labels must be unique within project - creating a second
    season with the same season value should raise an error."""

    prj_cd = "LHA_IA11_123"
    project = FN011Factory(prj_cd=prj_cd)
    ssn = "11"
    ssn_des = "Early Summer"

    ssn_date0 = datetime(2011, 6, 1)
    ssn_date1 = datetime(2011, 6, 25)

    ssn1 = FN022(
        project=project,
        ssn=ssn,
        ssn_des=ssn_des,
        ssn_date0=ssn_date0,
        ssn_date1=ssn_date1,
    )
    ssn1.save()
    ssn2 = FN022(
        project=project,
        ssn=ssn,
        ssn_des=ssn_des,
        ssn_date0=ssn_date0,
        ssn_date1=ssn_date1,
    )

    with pytest.raises(IntegrityError) as excinfo:
        ssn2.save()

    msg = "duplicate key value violates unique constraint"
    assert msg in str(excinfo.value)


@pytest.mark.xfail
def test_switched_dates():
    """If the season end date occured before the start date and error
    should be thrown."""
    assert 0 == 1


@pytest.mark.xfail
def test_dates_of_bounds():
    """The start and end date of each season must be withing teh bounds of
    the associated project.  If either is outside of the project start or
    end date, an error should be raised.

    """
    assert 0 == 1


@pytest.mark.xfail
def test_overlapping_seasons():
    """IF the seasons overlap, an error should be thrown."""
    assert 0 == 1
