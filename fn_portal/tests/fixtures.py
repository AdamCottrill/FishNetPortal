import pytest

from datetime import datetime, time

from ..models import FN123

from .factories import (
    UserFactory,
    SpeciesFactory,
    LakeFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
)


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

    setdate = datetime(2019, 9, 15)
    liftdate = datetime(2019, 9, 16)

    settime = time(10, 30)
    lifttime = time(15, 15)

    net1 = FN121Factory(
        sam="1",
        gr="GL00",
        sidep=25,
        effdur=24.1211,
        project=project,
        orient=1,
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
        gr="TP99",
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
