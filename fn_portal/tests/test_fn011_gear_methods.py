"""=============================================================
~/fn_portal/tests/test_fn011_gear_methods.py
 Created: 22 May 2020 11:30:41


 DESCRIPTION:

  This script contains a number of tests of the gear methods
  available on the FN011 model

 A. Cottrill
=============================================================

"""

import pytest

from .factories import FN028Factory, GearFactory
from .fixtures import project


@pytest.mark.django_db
def test_fn011_get_gear(project):
    """the gears listed should be GL00 and TP00"""

    gear1 = GearFactory(gr_code="GL00")
    gear2 = GearFactory(gr_code="TP99")

    FN028Factory(gear=gear1, project=project)
    FN028Factory(gear=gear2, project=project)

    gears = project.get_gear()
    assert gear1 in gears
    assert gear2 in gears


@pytest.mark.django_db
def test_fn011_get_121_gear_codes(project):
    """The get_121_gear_codes method should return a list of distinct gear
    codes used in the FN121 records for this project.

    """
    expected = ["GL00", "TP99"]
    assert set(project.get_121_gear_codes()) == set(expected)
