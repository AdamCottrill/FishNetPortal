"""
This fixture script creates several projects with known attributes and returns
those as a fixture  that is used to verify the api filters work as expected and
returns the correct records.

The list of projects is also used to create fixtures for each child table from
FN121 to lamprey, tags, age estimates, and diet items. The api endpoints for
these child  entities can also be filtered based on the attributes of the project.
By using the same project fixture, and creating one child record for each
project, we can re-use the parameters array in the test file to ensure that all
of the children can be filtered by attributes of the project they were collected
in.


"""

from fn_portal.tests.factories.common_factories import SpeciesFactory
import pytest

from datetime import date

from ...factories import (
    LakeFactory,
    SpeciesFactory,
    UserFactory,
    FNProtocolFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN125Factory,
    FN127Factory,
)


@pytest.fixture
def projects():
    """create several projects with known attributes and return them in an
    array"""

    homer = UserFactory(username="hsimpson")
    barney = UserFactory(username="bgumble")

    lake_superior = LakeFactory(lake_name="Lake Superior", abbrev="SU")
    lake_huron = LakeFactory(lake_name="Lake Huron", abbrev="HU")
    lake_erie = LakeFactory(lake_name="Lake Erie", abbrev="ER")
    lake_ontario = LakeFactory(lake_name="Lake Ontario", abbrev="ON")

    bsm = FNProtocolFactory(label="Broadscale Monitoring", abbrev="BSM")
    fwin = FNProtocolFactory(label="Fall Walleye Index Netting", abbrev="FWIN")
    nscin = FNProtocolFactory(label="Nearshore Community Index Netting", abbrev="NSCIN")
    oscin = FNProtocolFactory(label="Offshore Community Index Netting", abbrev="OSCIN")

    project0 = FN011Factory(
        prj_cd="LOA_IA10_000",
        prj_nm="Cool Project - 1",
        prj_ldr=homer,
        lake=lake_ontario,
        protocol=bsm,
        year=2010,
        prj_date0=date(2010, 10, 10),
        prj_date1=date(2010, 10, 17),
    )

    project1 = FN011Factory(
        prj_cd="LOA_IA10_111",
        prj_nm="Cool Project - 2",
        prj_ldr=homer,
        lake=lake_ontario,
        protocol=bsm,
        year=2010,
        prj_date0=date(2010, 10, 1),
        prj_date1=date(2010, 10, 10),
    )

    project2 = FN011Factory(
        prj_cd="LHA_IA12_222",
        prj_nm="Huron Project",
        prj_ldr=barney,
        lake=lake_huron,
        protocol=fwin,
        year=2012,
        prj_date0=date(2012, 10, 10),
        prj_date1=date(2012, 10, 17),
    )

    project3 = FN011Factory(
        prj_cd="LEA_IA13_333",
        prj_nm="Erie Project",
        prj_ldr=barney,
        lake=lake_erie,
        protocol=bsm,
        year=2013,
        prj_date0=date(2013, 10, 1),
        prj_date1=date(2013, 10, 10),
    )

    project4 = FN011Factory(
        prj_cd="LSA_IA08_444",
        prj_nm="Superior Project",
        prj_ldr=barney,
        lake=lake_superior,
        protocol=oscin,
        year=2008,
        prj_date0=date(2008, 10, 10),
        prj_date1=date(2008, 10, 17),
    )

    project5 = FN011Factory(
        prj_cd="LSA_IA07_555",
        prj_nm="Superior Project - 2",
        prj_ldr=homer,
        lake=lake_superior,
        protocol=nscin,
        year=2007,
        prj_date0=date(2007, 10, 1),
        prj_date1=date(2007, 10, 10),
    )

    return [project0, project1, project2, project3, project4, project5]


@pytest.fixture
def netsets(projects):
    """Create one net set for each project - in the same order as the projects array."""
    items = []

    for item in projects:
        items.append(FN121Factory(project=item))
    return items


@pytest.fixture
def efforts(netsets):
    """Create one effort for each net set - in the same order as the projects array."""
    items = []

    for item in netsets:
        items.append(FN122Factory(sample=item))
    return items


@pytest.fixture
def catchcounts(efforts):
    """Create catch count for each effort  - in the same order as the projects array."""

    species = SpeciesFactory(spc="091")

    items = []

    for item in efforts:
        items.append(FN123Factory(effort=item, species=species))
    return items


@pytest.fixture
def fish(catchcounts):
    """Create fish for each catch - in the same order as the projects array."""

    items = []

    for item in catchcounts:
        items.append(FN125Factory(catch=item))
    return items


@pytest.fixture
def age_estimates(fish):
    """Create one age estimate for each fish - in the same order as the projects array."""

    items = []

    for item in fish:
        items.append(FN127Factory(fish=item))
    return items
