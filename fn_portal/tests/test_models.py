import pytest

from .factories import (
    SpeciesFactory,
    FN011Factory,
    FN013Factory,
    FN014Factory,
    FN022Factory,
    FN026Factory,
    FN028Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
    FN124Factory,
    FN125Factory,
    FN126Factory,
    FN125TagFactory,
    FN125LampreyFactory,
    FN127Factory,
    GearFamilyFactory,
    GearFactory,
    SubGearFactory,
    Gear2SubGearFactory,
    GearEffortProcessTypeFactory,
    ProjectGearProcessTypeFactory,
)


@pytest.mark.django_db
def test_FN011_str():
    """
    Verify that the string representation of a FN011 object is the project
    name followed by the project code in brackets.
    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name)
    assert str(obj) == "{} ({})".format(project_name, project_code)


year_values = [None, ""]


@pytest.mark.django_db
@pytest.mark.parametrize("year", year_values)
def test_FN011_year_on_save(year):
    """The Fn011 model has a custom save function that creates the slug
    and populates the year if it is null or an empty string.  Verify that it works.

    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name, year=year)
    assert obj.year == "2000"


@pytest.mark.django_db
def test_FN011_slug_on_save():
    """The Fn011 model has a custom save function that creates the slug
    from the project code

    """

    project_code = "LHA_IA00_123"
    project_name = "Offshore Assessment"

    obj = FN011Factory(prj_cd=project_code, prj_nm=project_name)
    assert obj.slug == project_code.lower()


@pytest.mark.django_db
def test_FN022_str():
    """Verify that a sesaon is represented by object type, season description,
    season code, project code and for the associated project."""

    ssn = "11"
    ssn_des = "Early Summer"
    prj_cd = "LHA_IA11_123"

    project = FN011Factory.build(prj_cd=prj_cd)
    season = FN022Factory.build(project=project, ssn=ssn, ssn_des=ssn_des)

    shouldbe = "<Season: {} ({}) [{}]>".format(ssn_des, ssn, prj_cd)

    assert str(season) == shouldbe


def test_FN026_str():
    """Verify that a spatial strata are represented by object type,
    the space description, the space code and the project code
    and for the associated project."""

    prj_cd = "LHA_IA11_123"
    space = "AB"
    space_des = "the river"
    project = FN011Factory.build(prj_cd=prj_cd)

    spatial_strata = FN026Factory.build(
        project=project, space=space, space_des=space_des
    )
    shouldbe = "<Space: {} ({}) [{}]>".format(space_des, space, prj_cd)

    assert str(spatial_strata) == shouldbe


def test_FN028_str():
    """Verify that a fishing mode is represented by object type,
    the mode description, the mode code and the project code
    and for the associated project."""

    prj_cd = "LHA_SC11_123"
    mode = "AB"
    mode_des = "trolling"
    project = FN011Factory.build(prj_cd=prj_cd)

    fishing_mode = FN028Factory.build(project=project, mode=mode, mode_des=mode_des)
    shouldbe = "<FishingMode: {} ({}) [{}]>".format(mode_des, mode, prj_cd)

    assert str(fishing_mode) == shouldbe


@pytest.mark.django_db
def test_FN121_str():
    """
    Verify that the string representation of a FN121 object is the project
    code followed by the sample number separated by a dash.

    e.g. - LHA_IA00_123-001

    """

    project_code = "LHA_IA00_123"
    sam = 52

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    shouldbe = "{}-{}".format(project_code, sam)
    assert str(fn121) == shouldbe


@pytest.mark.django_db
def test_FN122_str():
    """
    Verify that the string representation of a FN122 object is the project
    code followed by sample number and effort each separated by a dash.

    e.g. - LHA_IA00_123-001-051

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    shouldbe = "{}-{}-{}".format(project_code, sam, eff)
    assert str(fn122) == shouldbe


@pytest.mark.django_db
def test_FN123_str():
    """Verify that the string representation of a FN123 object is the
    project code followed by sample number, effort, species code, and
    group code each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)

    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)

    shouldbe = "{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp)
    assert str(fn123) == shouldbe


@pytest.mark.django_db
def test_FN124_str():
    """
    Verify that the string representation of a FN124 object is the
    project code followed by sample number, effort, species code,
    group code and size calss each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00-350

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    siz = 350

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn124 = FN124Factory(catch=fn123, siz=siz)

    shouldbe = "{}-{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp, siz)
    assert str(fn124) == shouldbe


@pytest.mark.django_db
def test_FN125_str():
    """
    Verify that the string representation of a FN125 object is the
    project code followed by sample number, effort, species code,
    group code and fish number each separated by a dash.

    e.g. - LHA_IA00_123-001-051-091-00-1

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)

    shouldbe = "{}-{}-{}-{}-{}-{}".format(project_code, sam, eff, spc, grp, fish_number)
    assert str(fn125) == shouldbe


@pytest.mark.django_db
def test_FN126_str():
    """Verify that the string representation of a field collected diet
    item is the string reprentation of the associated
    fish, the food id, the taxon, and foodcount (in brackets)

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (F121: 3)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    food = 1
    taxon = "F121"
    foodcnt = 8

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    fn126 = FN126Factory(fish=fn125, food=food, taxon=taxon, foodcnt=foodcnt)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} ({}: {})".format(
        project_code, sam, eff, spc, grp, fish_number, food, taxon, foodcnt
    )

    assert str(fn126) == shouldbe


@pytest.mark.django_db
def test_FN127_str():
    """Verify that the string representation of a FN127 object is the
    string reprentation of the associated fish, the assigned age and
    the ageid. The fish and ageid are separated by a dash, the age
    estimate is prefixed with age= and is wrapped in brackets.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (age=4)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    ageid = 12
    age = 8

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    fn127 = FN127Factory(fish=fn125, ageid=ageid, agea=age)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (age={})".format(
        project_code, sam, eff, spc, grp, fish_number, ageid, age
    )

    assert str(fn127) == shouldbe


@pytest.mark.django_db
def test_FN125Tags_str():
    """Verify that the string representation of a FN_Tags object is the
    string reprentation of the associated fish, the tag number and the
    tag documentation string. The fish and tag number are separated by
    a dash, the tagdoc string is wrapped in brackets.

    e.g. - LHA_IA00_123-001-051-091-00-1-65984 (25012)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    fish_tag_id = 11
    tagnumber = 78910
    tagdoc = 12345

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    tag = FN125TagFactory(
        fish=fn125, fish_tag_id=fish_tag_id, tagid=tagnumber, tagdoc=tagdoc
    )

    shouldbe = "{}-{}-{}-{}-{}-{}-{} ({} ({}))".format(
        project_code, sam, eff, spc, grp, fish_number, fish_tag_id, tagnumber, tagdoc
    )

    assert str(tag) == shouldbe


@pytest.mark.django_db
def test_FN125Lamprey_xlam_str():
    """Verify that the string representation of a lamprey wound object is the
    string reprentation of the associated fish, the wound number and the
    xlam string.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (xlam: 0101)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    lamid = 11
    xlam = "0101"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    lamprey = FN125LampreyFactory(fish=fn125, lamid=lamid, xlam=xlam)

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (xlam: {})".format(
        project_code, sam, eff, spc, grp, fish_number, lamid, xlam
    )

    assert str(lamprey) == shouldbe


@pytest.mark.django_db
def test_FN125Lamprey_lamijc_str():
    """Verify that the string representation of a lamprey wound object is the
    string reprentation of the associated fish, the wound number and the
    lamijc string.

    e.g. - LHA_IA00_123-001-051-091-00-1-1 (lamijc: A235)

    """

    project_code = "LHA_IA00_123"
    sam = "001"
    eff = "051"
    spc = 334
    species = SpeciesFactory(spc=spc)
    grp = "55"
    fish_number = 9
    lamid = 11
    lamijc_type = "A1"
    lamijc_size = "25"

    project = FN011Factory(prj_cd=project_code)
    fn121 = FN121Factory(project=project, sam=sam)
    fn122 = FN122Factory(sample=fn121, eff=eff)
    fn123 = FN123Factory(effort=fn122, species=species, grp=grp)
    fn125 = FN125Factory(catch=fn123, fish=fish_number)
    lamprey = FN125LampreyFactory(
        fish=fn125, lamid=lamid, lamijc_size=lamijc_size, lamijc_type=lamijc_type
    )

    shouldbe = "{}-{}-{}-{}-{}-{}-{} (lamijc: {}{})".format(
        project_code, sam, eff, spc, grp, fish_number, lamid, lamijc_type, lamijc_size
    )

    assert str(lamprey) == shouldbe


@pytest.mark.django_db
def test_FN013_str():
    """Verify that the string representation of a FN013 object is the
    project the gear code, followed by the project code of the
    associated project.  The project code should be wrapped in
    brackets.

    """

    project_code = "LHA_IA00_123"
    gear_code = "GL99"

    project = FN011Factory(prj_cd=project_code)
    fn013 = FN013Factory(project=project, gr=gear_code)
    assert str(fn013) == "{} ({})".format(gear_code, project_code)


@pytest.mark.django_db
def test_FN014_str():
    """Verify that the string representation of a FN014 object is the gear
    code, followed by the effort (mesh size), folled by the project code
    of the associated project.  The gear code and mesh size are
    separted by a dash, while the project code should be wrapped in
    brackets.

    """

    project_code = "LHA_IA00_123"
    gear_code = "GL99"
    effort = "99"

    project = FN011Factory(prj_cd=project_code)
    fn013 = FN013Factory(project=project, gr=gear_code)
    fn014 = FN014Factory(gear=fn013, eff=effort)

    assert str(fn014) == "{}-{} ({})".format(gear_code, effort, project_code)


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
    family = GearFamilyFactory(family=family_label, abbrev=abbrev)
    subgear = SubGearFactory(family=family, eff=eff)

    assert str(subgear) == "{} ({} ({}))".format(eff, family_label, abbrev)


@pytest.mark.django_db
def test_Gear2SubGear_str():
    """Verify that the string representation of a Gear2Subgear object is
    the string representation of the gear followed by the subgear,
    separated by a dash.
    """

    family_label = "Offshore Index"
    abbrev = "osi"
    eff = "089"

    gr_label = "6' Trapnet"
    gr_code = "TP06"

    gear = GearFactory(gr_label=gr_label, gr_code=gr_code)

    family = GearFamilyFactory(family=family_label, abbrev=abbrev)
    subgear = SubGearFactory(family=family, eff=eff)

    gear2subgear = Gear2SubGearFactory(gear=gear, subgear=subgear)

    gear_part = "{} ({})".format(gr_label, gr_code)
    subgear_part = "{} ({} ({}))".format(eff, family_label, abbrev)

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
