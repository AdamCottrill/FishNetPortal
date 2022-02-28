import pytest
from django.core.exceptions import ValidationError
from fn_portal.models import FN012, FN012Protocol

from ..factories import FN011Factory, SpeciesFactory, LakeFactory, FNProtocolFactory


@pytest.fixture()
def project():
    project = FN011Factory()
    return project


@pytest.fixture()
def species():
    species = SpeciesFactory()
    return species


@pytest.fixture()
def lake():
    lake = LakeFactory()
    return lake


@pytest.fixture()
def protocol():
    protocol = FNProtocolFactory()
    return protocol


@pytest.mark.django_db
def test_FN012_str(project, species):
    """verify that the string representation of an fn012 object is of the form:
    fn012-{prj_cd}-{spc}-{grp}"
    """

    prj_cd = project.prj_cd
    spc = species.spc
    grp = "55"

    fn012 = FN012(project=project, species=species, grp=grp)
    fn012.save()

    expected = f"fn012-{prj_cd}-{spc}-{grp}"
    assert str(fn012) == expected.lower()


@pytest.mark.django_db
def test_FN012_default_str(lake, protocol, species):
    """verify that the string representation of an protocol default FN012 is of the form:
    fn012-{lake}-{protocol}-{spc}-{grp}"""

    protocol_abbrev = protocol.abbrev
    lake_abbrev = lake.abbrev
    spc = species.spc
    grp = "55"

    fn012 = FN012Protocol(lake=lake, protocol=protocol, species=species, grp=grp)
    fn012.save()

    expected = f"fn012default-{lake_abbrev}-{protocol_abbrev}-{spc}-{grp}"
    assert str(fn012) == expected.lower()


@pytest.mark.django_db
def test_FN012_duplicate(project, species):
    """FN012 records must be unique within projects. If we try to save two
    records for the same project, species, and group, an integrity error
    should be raised."""

    prj_cd = project.prj_cd
    spc = species.spc
    grp = "55"

    fn012a = FN012(project=project, species=species, grp=grp)
    fn012a.save()

    fn012b = FN012(project=project, species=species, grp=grp)

    with pytest.raises(ValidationError) as excinfo:
        fn012b.save()
    msg = "this Slug already exists"
    assert msg in str(excinfo.value)


@pytest.mark.django_db
def test_FN012_default_duplicate(protocol, lake, species):
    """the Protocol default FN012 records must be unique within protocols
    and lakes. If we try to save two records for the same
    protocol, lake, species, and group an integrity error should be
    raised.

    """

    protocol_abbrev = protocol.abbrev
    lake_abbrev = lake.abbrev
    spc = species.spc
    grp = "55"

    fn012a = FN012Protocol(lake=lake, protocol=protocol, species=species, grp=grp)
    fn012a.save()

    fn012b = FN012Protocol(lake=lake, protocol=protocol, species=species, grp=grp)

    with pytest.raises(ValidationError) as excinfo:
        fn012b.save()
    msg = "this Slug already exists"
    assert msg in str(excinfo.value)


fdsam_agedec_spcmrk_list = [("1", "2", "12"), ("0", None, "0")]


@pytest.mark.django_db
@pytest.mark.parametrize("fdsam1,fdsam2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_fdsam(project, species, fdsam1, fdsam2, expected):
    """The FN012 base model has a property that returns the value of fdsam
    as a concatentation of fdsam1 and fdsam2.  fsdsam2 should only be
    returned if it is not empty.

    """
    fn012 = FN012(
        project=project,
        species=species,
        grp="00",
        fdsam1=fdsam1,
        fdsam2=fdsam2,
    )
    assert fn012.fdsam == expected


@pytest.mark.django_db
@pytest.mark.parametrize("fdsam1,fdsam2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_default_fdsam(lake, protocol, species, fdsam1, fdsam2, expected):
    """The FN012 base model has a property that returns the value of fdsam
    as a concatentation of fdsam1 and fdsam2.  fsdsam2 should only be
    returned if it is not empty."""

    fn012 = FN012Protocol(
        lake=lake,
        protocol=protocol,
        species=species,
        grp="00",
        fdsam1=fdsam1,
        fdsam2=fdsam2,
    )
    assert fn012.fdsam == expected


@pytest.mark.django_db
@pytest.mark.parametrize("spcmrk1,spcmrk2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_spcmrk(project, species, spcmrk1, spcmrk2, expected):
    """The FN012 base model has a property that returns the value of spcmrk
    as a concatentation of spcmrk1 and spcmrk2.  fsdsam2 should only be
    returned if it is not empty.

    """
    fn012 = FN012(
        project=project,
        species=species,
        grp="00",
        spcmrk1=spcmrk1,
        spcmrk2=spcmrk2,
    )
    assert fn012.spcmrk == expected


@pytest.mark.django_db
@pytest.mark.parametrize("spcmrk1,spcmrk2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_default_spcmrk(lake, protocol, species, spcmrk1, spcmrk2, expected):
    """The FN012 base model has a property that returns the value of spcmrk
    as a concatentation of spcmrk1 and spcmrk2.  fsdsam2 should only be
    returned if it is not empty."""

    fn012 = FN012Protocol(
        lake=lake,
        protocol=protocol,
        species=species,
        grp="00",
        spcmrk1=spcmrk1,
        spcmrk2=spcmrk2,
    )
    assert fn012.spcmrk == expected


@pytest.mark.django_db
@pytest.mark.parametrize("agedec1,agedec2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_agedec(project, species, agedec1, agedec2, expected):
    """The FN012 base model has a property that returns the value of agedec
    as a concatentation of agedec1 and agedec2.  fsdsam2 should only be
    returned if it is not empty.

    """
    fn012 = FN012(
        project=project,
        species=species,
        grp="00",
        agedec1=agedec1,
        agedec2=agedec2,
    )
    assert fn012.agedec == expected


@pytest.mark.django_db
@pytest.mark.parametrize("agedec1,agedec2,expected", fdsam_agedec_spcmrk_list)
def test_FN012_default_agedec(lake, protocol, species, agedec1, agedec2, expected):
    """The FN012 base model has a property that returns the value of agedec
    as a concatentation of agedec1 and agedec2.  fsdsam2 should only be
    returned if it is not empty."""

    fn012 = FN012Protocol(
        lake=lake,
        protocol=protocol,
        species=species,
        grp="00",
        agedec1=agedec1,
        agedec2=agedec2,
    )
    assert fn012.agedec == expected


invalid_args = [
    ("agedec", {"agedec1": "0", "agedec2": "2"}),
    ("agedec", {"agedec1": 2, "agedec2": None}),
    ("fdsam", {"fdsam1": 0, "fdsam2": 2}),
    ("fdsam", {"fdsam1": 2, "fdsam2": None}),
    ("spcmrk", {"spcmrk1": 0, "spcmrk2": 2}),
    ("spcmrk", {"spcmrk1": 2, "spcmrk2": None}),
]


@pytest.mark.django_db
@pytest.mark.parametrize("field,args", invalid_args)
def test_FN012_invalid(project, species, field, args):
    """The FN012 model has several validation checks that need to be verifyied:

    + if agedec1 is 0, agedec2 must be null,
    + if agedec1 is not 0, agedec2 must not be null,

    + if fdsam1 is 0, fdsam2 must be null,
    + if fdsam1 is not 0, fdsam2 must not be null,

    + if spcmrk1 is 0, spcmrk2 must be null,
    + if spcmrk1 is not 0, spcmrk2 must not be null,

    """

    fn012 = FN012(project=project, species=species, grp="00", **args)

    with pytest.raises(ValidationError) as excinfo:
        fn012.save()

    msg = f"Invalid {field.upper()} code"
    assert msg in str(excinfo.value)


@pytest.mark.django_db
@pytest.mark.parametrize("field,args", invalid_args)
def test_FN012_default_invalid(lake, protocol, species, field, args):
    """The FN012 model has several validation checks that need to be verifyied:

    + if agedec1 is 0, agedec2 must be null,
    + if agedec1 is not 0, agedec2 must not be null,

    + if fdsam1 is 0, fdsam2 must be null,
    + if fdsam1 is not 0, fdsam2 must not be null,

    + if spcmrk1 is 0, spcmrk2 must be null,
    + if spcmrk1 is not 0, spcmrk2 must not be null,

    """

    fn012 = FN012Protocol(
        lake=lake, protocol=protocol, species=species, grp="00", **args
    )

    with pytest.raises(ValidationError) as excinfo:
        fn012.save()

    msg = f"Invalid {field.upper()} code"
    assert msg in str(excinfo.value)
