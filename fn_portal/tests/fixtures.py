from datetime import datetime, time

import pytest
from _pytest.fixtures import get_direct_param_fixture_func

from ..models import FN123
from .factories import (
    FN011Factory,
    FN013Factory,
    FN014Factory,
    FN022Factory,
    FN026Factory,
    FN028Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
    GearFactory,
    LakeFactory,
    SpeciesFactory,
    UserFactory,
)

SCOPE = "function"


@pytest.fixture(scope=SCOPE)
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def project():
    """fixture to setup a basic project - two net sets with three species in each."""

    perch = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )
    pike = SpeciesFactory(spc="131", spc_nmco="Pike", spc_nmsc="Esox lucius")
    walleye = SpeciesFactory(spc="334", spc_nmco="Walleye", spc_nmsc="Sander vitreus")
    anyspc = SpeciesFactory(spc="000", spc_nmco="AnySpecies", spc_nmsc=None)

    prj_cd = "LHA_IA19_000"
    project = FN011Factory(prj_cd=prj_cd, prj_nm="Test Project")

    gl01 = FN013Factory(
        project=project, gr="GL01", effcnt=3, effdst=300, gr_des="Multifilament"
    )

    FN013Factory(
        project=project, gr="GL32", effcnt=8, effdst=400, gr_des="Monofilament"
    )

    FN014Factory(gear=gl01, eff="038", mesh=38, grlen=100)
    FN014Factory(gear=gl01, eff="051", mesh=51, grlen=100)
    FN014Factory(gear=gl01, eff="064", mesh=64, grlen=100)

    ssn = "32"
    ssn_des = "August"
    ssn_date0 = datetime.strptime("2019-08-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2019-08-31", "%Y-%m-%d")
    FN022Factory(
        project=project,
        ssn=ssn,
        ssn_des=ssn_des,
        ssn_date0=ssn_date0,
        ssn_date1=ssn_date1,
        __sequence=1,
    )

    ssn = "33"
    ssn_des = "September"
    ssn_date0 = datetime.strptime("2019-09-01", "%Y-%m-%d")
    ssn_date1 = datetime.strptime("2019-09-30", "%Y-%m-%d")
    FN022Factory(
        project=project,
        ssn=ssn,
        ssn_des=ssn_des,
        ssn_date0=ssn_date0,
        ssn_date1=ssn_date1,
    )

    FN026Factory(
        project=project,
        space="S1",
        space_des="Space 1",
        dd_lat=45.1,
        dd_lon=-81.1,
        __sequence=1,
    )
    FN026Factory(
        project=project, space="S2", space_des="Space 2", dd_lat=45.2, dd_lon=-81.2
    )

    gl00 = GearFactory(gr_code="GL00", grtp="GL")
    mode1 = FN028Factory(
        project=project, mode="m1", gear=gl00, orient=1, mode_des="Mode 1", __sequence=1
    )

    tp99 = GearFactory(gr_code="TP99", grtp="TP")
    mode2 = FN028Factory(project=project, mode="m2", mode_des="Mode 2", gear=tp99)

    setdate = datetime(2019, 9, 15)
    liftdate = datetime(2019, 9, 16)

    settime = time(10, 30)
    lifttime = time(15, 15)

    net1 = FN121Factory(
        sam="1",
        mode=mode1,
        sidep=25,
        effdur=24.1211,
        project=project,
        effdt0=setdate,
        effdt1=liftdate,
        efftm0=settime,
        efftm1=lifttime,
    )
    eff1 = FN122Factory(sample=net1)

    FN123Factory(effort=eff1, species=perch, catcnt=3, biocnt=0)
    FN123Factory(effort=eff1, species=pike, catcnt=6, biocnt=2)
    FN123Factory(effort=eff1, species=walleye, catcnt=9, biocnt=3)
    FN123Factory(effort=eff1, species=anyspc, catcnt=None)

    net2 = FN121Factory(
        sam="2",
        mode=mode2,
        sidep=5,
        effdur=22.5,
        project=project,
        effdt0=setdate,
        effdt1=liftdate,
    )
    eff2 = FN122Factory(sample=net2)

    FN123Factory(effort=eff2, species=perch, catcnt=1, biocnt=0)
    FN123Factory(effort=eff2, species=pike, catcnt=2, biocnt=2)
    FN123Factory(effort=eff2, species=walleye, catcnt=3, biocnt=3)
    FN123Factory(effort=eff2, species=anyspc, catcnt=None)

    return project


@pytest.fixture
def somefish(project):
    """Add some fish to our project fixture - for those test that need it."""

    fn123 = FN123.objects.get(
        effort__sample__project=project, effort__sample__sam=1, species__spc="334"
    )

    fish1 = FN125Factory(catch=fn123)
    fish2 = FN125Factory(catch=fn123)

    return [fish1, fish2]


@pytest.fixture
def project_list():
    """fixture to setup some basic projects (wihtout any net sets) to
    verify that our project list and associated filters are working as
    expected.

    """

    homer = UserFactory(first_name="Homer", last_name="Simpson")
    barney = UserFactory(first_name="Barney", last_name="Gumble")

    huron = LakeFactory(lake_name="Huron", abbrev="HU")
    superior = LakeFactory(lake_name="Superior", abbrev="SU")

    project0 = FN011Factory(
        prj_cd="LHA_IA19_000",
        prj_nm="Test Project A",
        lake=huron,
        prj_ldr=homer,
        year=2019,
        source="smallfish",
    )

    project1 = FN011Factory(
        prj_cd="LHA_IA10_111",
        prj_nm="Test Project A",
        lake=huron,
        prj_ldr=homer,
        year=2010,
        source="nearshore",
    )

    project2 = FN011Factory(
        prj_cd="LSA_IA15_222",
        prj_nm="Test Project B",
        lake=superior,
        prj_ldr=homer,
        year=2015,
        source="offshore",
    )

    project3 = FN011Factory(
        prj_cd="LHA_IA19_333",
        prj_nm="Test Project C",
        lake=huron,
        prj_ldr=homer,
        year=2019,
        source="offshore",
    )

    project4 = FN011Factory(
        prj_cd="LSA_IA10_444",
        prj_nm="Test Project D - findme",
        lake=superior,
        prj_ldr=barney,
        year=2010,
        source="offshore",
    )

    project5 = FN011Factory(
        prj_cd="LHA_IA15_555",
        prj_nm="Test Project E - FINDME",
        lake=huron,
        prj_ldr=barney,
        year=2015,
        source="nearshore",
    )

    project6 = FN011Factory(
        prj_cd="LHA_IA19_666",
        prj_nm="Test Project F - FindMe",
        lake=huron,
        prj_ldr=barney,
        year=2019,
        source="offshore",
    )

    return [project0, project1, project2, project3, project4, project5, project6]
