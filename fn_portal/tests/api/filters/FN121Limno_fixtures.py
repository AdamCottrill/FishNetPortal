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
        sample=sample1, do_gear=8.1, xo2=None, xo22=10.5, surfdo2=5.7, surfdo22=None
    )

    sample2 = FN121Factory(project=project)
    limno2 = FN121LimnoFactory(
        sample=sample2, do_gear=9.1, xo2=None, xo22=8.5, surfdo2=None, surfdo22=11.3
    )

    sample3 = FN121Factory(project=project)
    limno3 = FN121LimnoFactory(
        sample=sample3, do_gear=14.0, xo2=1.1, xo22=None, surfdo2=6.7, surfdo22=9.3
    )

    sample4 = FN121Factory(project=project)
    limno4 = FN121LimnoFactory(
        sample=sample4, do_gear=4.0, xo2=2.2, xo22=None, surfdo2=7.7, surfdo22=7.3
    )

    sample5 = FN121Factory(project=project)
    limno5 = FN121LimnoFactory(
        sample=sample5, do_gear=None, xo2=3.3, xo22=7.5, surfdo2=None, surfdo22=5.3
    )

    sample6 = FN121Factory(project=project)
    limno6 = FN121LimnoFactory(
        sample=sample6, do_gear=None, xo2=4.4, xo22=6.5, surfdo2=8.7, surfdo22=None
    )

    return [limno1, limno2, limno3, limno4, limno5, limno6]
