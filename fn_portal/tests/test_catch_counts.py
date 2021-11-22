"""=============================================================
~/fn_portal/tests/test_catch_counts.py
 Created: 22 May 2020 09:05:07

 DESCRIPTION:

  This script contains a number of tests of the catch count methods
  available on the FN011 and FN121 models

 A. Cottrill
=============================================================

"""

import pytest

from fn_portal.models import FN121

from .factories import FN013Factory
from .fixtures import project


@pytest.mark.django_db
def test_fn011_total_catch(project):
    """This method should return the number of species caught in this
    project and the total number of fish.

    The total catch for our whole project is 24 fish.

    """

    assert project.total_catch() == {"spc_cnt": 3, "total": 24}


@pytest.mark.django_db
def test_fn011_catch_counts(project):
    """The catch counts function should retrun the total number of fish
    caught in this project by species.  It should not include an entry
    for '000'

    we caught three species in our project:
    + perch: catcnt = 4, biocnt=0
    + pike: catcnt = 8, biocnt=4
    + walleye: catcnt = 12, biocnt=6

    """

    # the expected return value is a list of dictionaries - one for
    # each species. Each dictionary should have the keys: species,
    # spc, catcnts, and biocnts.  The list of species should not
    # inlcude '000'

    expected = [
        {"species": "Yellow Perch", "spc": "331", "catcnts": 4, "biocnts": 0},
        {"species": "Pike", "spc": "131", "catcnts": 8, "biocnts": 4},
        {"species": "Walleye", "spc": "334", "catcnts": 12, "biocnts": 6},
    ]

    returned = list(project.catch_counts())

    assert len(returned) == len(expected)

    for item in expected:

        assert item in returned


@pytest.mark.django_db
def test_fn121_total_catch(project):
    """This method should return the total catch for an individual net set.

    Our first net caught 18 fish.
    """

    netset = FN121.objects.get(project=project, sam=1)
    assert netset.total_catch() == {"spc_cnt": 3, "total": 18}


@pytest.mark.django_db
def test_fn121_catch_counts(project):
    """The catch counts function should retrun the total number of fish
    caught by species in one net.  It should not include an entry
    for '000'

    our first net caught three species in our project:
    + perch: 3
    + pike: 6
    + walleye: 9


    """

    expected = [
        {"species": "Yellow Perch", "spc": "331", "catcnts": 3, "biocnts": 0},
        {"species": "Pike", "spc": "131", "catcnts": 6, "biocnts": 2},
        {"species": "Walleye", "spc": "334", "catcnts": 9, "biocnts": 3},
    ]

    netset = FN121.objects.get(project=project, sam=1)
    returned = list(netset.catch_counts())

    assert len(returned) == len(expected)

    from pprint import pprint

    pprint(returned)
    pprint(expected)

    for item in expected:
        assert item in returned
