import pytest
from django.core.exceptions import ValidationError

from ..factories import FN011Factory, FN121Factory, FN122Factory, FN123NonFishFactory

from ..fixtures import taxon_list


@pytest.mark.django_db
def test_FN123NonFish_str(taxon_list):
    """Verify that the string representation of a FN123NonFish object
    is the project code followed by the sample number, effort number
    and itis code all separated with a dash.

    e.g. - LHA_IA00_123-001-TRANSECT

    """

    project_code = "LHA_IA00_123"
    sam = 52
    effort = "001"
    taxon = taxon_list[0]

    project = FN011Factory(prj_cd=project_code)
    sample = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=sample, eff=effort)

    fn123nonfish = FN123NonFishFactory(effort=fn122, taxon=taxon)
    shouldbe = "{}-{}-{}-{}".format(project_code, sam, effort, taxon.itiscode)
    assert str(fn123nonfish) == shouldbe


@pytest.mark.django_db
def test_FN123NonFish_fn_keys(taxon_list):
    """Verify that the fishnet keys and object slug are comprised of
    the project code followed by the sample number, followed by
    effort, followed by transect code, all separated by a dash:

    e.g. - lha_ia00_123-001-1

    """

    project_code = "LHA_IA00_123"
    sam = 52
    effort = "001"
    taxon = taxon_list[0]

    project = FN011Factory(prj_cd=project_code)
    sample = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=sample, eff=effort)

    fn123nonfish = FN123NonFishFactory(effort=fn122, taxon=taxon)
    shouldbe = "{}-{}-{}-{}".format(project_code, sam, effort, taxon.itiscode)

    assert fn123nonfish.slug == shouldbe.lower()
    assert fn123nonfish.fishnet_keys() == shouldbe


invalid_args = [
    ("catcnt", -1, "Ensure this value is greater than or equal to 1."),
    ("mortcnt", -1, "Ensure this value is greater than or equal to 0."),
    ("mortcnt", 999, "mortcnt cannot be greater than catcnt."),
]


@pytest.mark.django_db
@pytest.mark.parametrize("fld,value,msg", invalid_args)
def test_Fn123nonfish_parameter_outside_bounds(taxon_list, fld, value, msg):
    """Catcnt and mortcnt both have validators associated with them -
    both must be positive.  Catcnt must be at least 1.  Mort count
    cannot be negative, and mortcnt cannot be greater than catcnt.
    """

    data = {}
    data[fld] = value

    project = FN011Factory()
    fn121 = FN121Factory()
    fn122 = FN122Factory(sample=fn121)
    taxon = taxon_list[0]

    with pytest.raises(ValidationError) as excinfo:
        fn123nonfish = FN123NonFishFactory(effort=fn122, taxon=taxon, **data)
        fn123.save()

    assert msg in str(excinfo.value)
