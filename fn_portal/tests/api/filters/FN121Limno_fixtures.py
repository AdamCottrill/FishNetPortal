"""

"""

import pytest
from ...factories import (
    FN011Factory,
    FN121Factory,
    FN121LimnoFactory,
)


@pytest.fixture
def limno_data():
    """create several sets of with known attributes and return them in an
    array"""

    project = FN011Factory()
    sample1 = FN121Factory(project=project)
    limno1 = FN121LimnoFactory(
        sample=sample1,
        o2gear0=8.1,
        o2gear1=8.1,
        o2bot0=None,
        o2bot1=10.5,
        o2surf0=5.7,
        o2surf1=None,
    )

    sample2 = FN121Factory(project=project)
    limno2 = FN121LimnoFactory(
        sample=sample2,
        o2gear0=9.1,
        o2gear1=9.1,
        o2bot0=None,
        o2bot1=8.5,
        o2surf0=None,
        o2surf1=11.3,
    )

    sample3 = FN121Factory(project=project)
    limno3 = FN121LimnoFactory(
        sample=sample3,
        o2gear0=14.0,
        o2gear1=14.0,
        o2bot0=1.1,
        o2bot1=None,
        o2surf0=6.7,
        o2surf1=9.3,
    )

    sample4 = FN121Factory(project=project)
    limno4 = FN121LimnoFactory(
        sample=sample4,
        o2gear0=4.0,
        o2gear1=4.0,
        o2bot0=2.2,
        o2bot1=None,
        o2surf0=7.7,
        o2surf1=7.3,
    )

    sample5 = FN121Factory(project=project)
    limno5 = FN121LimnoFactory(
        sample=sample5,
        o2gear0=None,
        o2gear1=None,
        o2bot0=3.3,
        o2bot1=7.5,
        o2surf0=None,
        o2surf1=5.3,
    )

    sample6 = FN121Factory(project=project)
    limno6 = FN121LimnoFactory(
        sample=sample6,
        o2gear0=None,
        o2gear1=None,
        o2bot0=4.4,
        o2bot1=6.5,
        o2surf0=8.7,
        o2surf1=None,
    )

    return [limno1, limno2, limno3, limno4, limno5, limno6]
