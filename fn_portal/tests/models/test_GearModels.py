import pytest

from ..factories import (
    FN011Factory,
    GearFamilyFactory,
    GearFactory,
    SubGearFactory,
    Gear2SubGearFactory,
    GearEffortProcessTypeFactory,
    ProjectGearProcessTypeFactory,
)


@pytest.mark.django_db
def test_GearFamily_str():
    """
    Verify that the string representation of a GearFamily object is the gear family
    name followed by the gear family abbreviation in brackets.
    """

    family = "Offshore Index"
    abbrev = "osi"

    gearfamily = GearFamilyFactory(family=family, abbrev=abbrev)

    assert str(gearfamily) == "{} ({})".format(family, abbrev)


@pytest.mark.django_db
def test_Gear_str():
    """
    Verify that the string representation of a Gear object is the gear label
    name followed by the gear code in brackets.

    """

    gr_label = "6' Trapnet"
    gr_code = "TP06"

    gear = GearFactory(gr_label=gr_label, gr_code=gr_code)

    assert str(gear) == "{} ({})".format(gr_label, gr_code)


@pytest.mark.django_db
def test_SubGear_str():
    """Verify that the string representation of a SubGear object is
    simply the eff value.

    """

    family_label = "Offshore Index"
    abbrev = "osi"
    eff = "089"
    mesh = 51
    grlen = 50
    grht = 1.8

    family = GearFamilyFactory(family=family_label, abbrev=abbrev)
    subgear = SubGearFactory(family=family, eff=eff, mesh=mesh, grlen=grlen, grht=grht)

    assert str(subgear) == "{}-{}-{}-{} ({} ({}))".format(
        eff, mesh, grlen, grht, family_label, abbrev
    )


@pytest.mark.django_db
def test_Gear2SubGear_str():
    """Verify that the string representation of a Gear2Subgear object is
    the string representation of the gear followed by the subgear,
    separated by a dash.
    """

    family_label = "Offshore Index"
    abbrev = "osi"
    eff = "089"
    mesh = 51
    grlen = 50
    grht = 1.8

    gr_label = "6' Trapnet"
    gr_code = "TP06"

    gear = GearFactory(gr_label=gr_label, gr_code=gr_code)

    family = GearFamilyFactory(family=family_label, abbrev=abbrev)

    subgear = SubGearFactory(family=family, eff=eff, mesh=mesh, grlen=grlen, grht=grht)
    gear2subgear = Gear2SubGearFactory(gear=gear, subgear=subgear)

    gear_part = "{} ({})".format(gr_label, gr_code)
    subgear_part = "{}-{}-{}-{} ({} ({}))".format(
        eff, mesh, grlen, grht, family_label, abbrev
    )

    assert str(gear2subgear) == gear_part + " - " + subgear_part


@pytest.mark.django_db
def test_GearEffortProcessType_str():
    """Verify that the string representation of a Gear Effort process type
    object is the gear code, followed by the effort, followed by the
    process type, each separated by a dash.

    """

    gear_code = "GL50"
    eff = "002"
    process_type = "3"

    gear = GearFactory(gr_code=gear_code)
    gear_process_type = GearEffortProcessTypeFactory.build(
        gear=gear, eff=eff, process_type=process_type
    )

    expected = f"{gear_code} - {process_type} - {eff}"

    assert str(gear_process_type) == expected


@pytest.mark.django_db
def test_GearEffortProcessType_str():
    """
    Verify that the string representation of a Project Gear Process
    Type object is the Project code, followed by the gear code,
    followed by the process type, each separated by a dash.

    """

    prj_cd = "LHA_IA00_123"
    gear_code = "GL50"
    process_type = "3"

    project = FN011Factory(prj_cd=prj_cd)
    gear = GearFactory(gr_code=gear_code)
    project_gear_process_type = ProjectGearProcessTypeFactory.build(
        project=project, gear=gear, process_type=process_type
    )

    expected = f"{prj_cd}-{gear_code}-{process_type}"

    assert str(project_gear_process_type) == expected
