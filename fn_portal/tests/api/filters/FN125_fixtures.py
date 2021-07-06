"""
This fixture script creates several fish with known attributes and returns those
as a fixture  that is used to verify the api filters work as expected and
returns the correct records.

The list of fish is also used to create fixtures for lamprey, tags age
estimates, and diet items. The api endpoints  for these enties can also be
filtered based on the attributes of the 'parent' fish.  By using the same fish
fixture, and creating one child record for each fish, we can re-use the
parameters array in the test file.
"""

import pytest

from ...factories import (
    FN123Factory,
    FN125Factory,
    FN125LampreyFactory,
    FN125TagFactory,
    FN126Factory,
    FN127Factory,
    SpeciesFactory,
)


@pytest.fixture
def fish():

    species1 = SpeciesFactory(spc="334")
    species2 = SpeciesFactory(spc="081")

    catch1 = FN123Factory(species=species1)
    catch2 = FN123Factory(species=species2)

    fish0 = FN125Factory(
        catch=catch2,
        flen=225,
        tlen=250,
        rwt=None,
        clipc="0",
        clipa=None,
        gon=None,
        mat=9,
        sex=9,
        noda="711",
        nodc="714",
    )
    fish1 = FN125Factory(
        catch=catch1,
        flen=275,
        tlen=300,
        rwt=500,
        clipc="2",
        clipa=None,
        gon=None,
        mat=None,
        sex=1,
        noda=None,
        nodc="714",
    )
    fish2 = FN125Factory(
        catch=catch2,
        flen=375,
        tlen=400,
        rwt=1000,
        clipc="5",
        clipa="5",
        gon=10,
        mat=1,
        sex=1,
        noda=None,
        nodc=None,
    )
    fish3 = FN125Factory(
        catch=catch1,
        flen=375,
        tlen=400,
        rwt=1100,
        clipc="0",
        clipa="7",
        gon=20,
        mat=2,
        sex=2,
        noda="716",
        nodc="716",
    )
    fish4 = FN125Factory(
        catch=catch2,
        flen=325,
        tlen=350,
        rwt=800,
        clipc="23",
        clipa="25",
        gon=30,
        mat=None,
        sex=None,
        noda="714",
        nodc="711",
    )
    fish5 = FN125Factory(
        catch=catch1,
        flen=225,
        tlen=250,
        rwt=500,
        clipc=None,
        clipa="2",
        gon=9,
        mat=9,
        sex=None,
        noda="711",
        nodc="711",
    )

    return [fish0, fish1, fish2, fish3, fish4, fish5]


@pytest.fixture
def fish_FN125Tags(fish):
    """Create one tag for each fish - in the same order as the fish array."""
    items = []

    for item in fish:
        items.append(FN125TagFactory(fish=item))
    return items


@pytest.fixture
def fish_FN125Lamprey(fish):
    """Create one lamprey wound for each fish - in the same order as the fish array."""
    items = []

    for item in fish:
        items.append(FN125LampreyFactory(fish=item))
    return items


@pytest.fixture
def fish_FN126(fish):
    """Create one fn126 record for each fish - in the same order as the fish array."""
    items = []

    for item in fish:
        items.append(FN126Factory(fish=item))
    return items


@pytest.fixture
def fish_FN127(fish):
    """Create one fn127 record for each fish - in the same order as the fish array."""
    items = []

    for item in fish:
        items.append(FN127Factory(fish=item))
    return items
