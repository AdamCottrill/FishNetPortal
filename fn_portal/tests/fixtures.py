import pytest

from .factories import (
    SpeciesFactory,
    FN011Factory,
    FN121Factory,
    FN122Factory,
    FN123Factory,
)


@pytest.fixture
def project():
    """ fixture to setup a basic project - two net sets with three species in each.
    """

    perch = SpeciesFactory(
        spc="331", spc_nmco="Yellow Perch", spc_nmsc="Perca flavescens"
    )
    pike = SpeciesFactory(spc="131", spc_nmco="Pike", spc_nmsc="Esox lucius")
    walleye = SpeciesFactory(spc="334", spc_nmco="Walleye", spc_nmsc="Sander vitreus")
    anyspc = SpeciesFactory(spc="000", spc_nmco="AnySpecies", spc_nmsc=None)

    prj_cd = "LHA_IA19_000"
    project = FN011Factory(prj_cd=prj_cd, prj_nm="Test Project")

    net1 = FN121Factory(sam="1", gr="GL00", project=project)
    eff1 = FN122Factory(sample=net1)

    FN123Factory(effort=eff1, species=perch, catcnt=3, biocnt=0)
    FN123Factory(effort=eff1, species=pike, catcnt=6, biocnt=2)
    FN123Factory(effort=eff1, species=walleye, catcnt=9, biocnt=3)
    FN123Factory(effort=eff1, species=anyspc, catcnt=None)

    net2 = FN121Factory(sam="2", gr="TP99", project=project)
    eff2 = FN122Factory(sample=net2)

    FN123Factory(effort=eff2, species=perch, catcnt=1, biocnt=0)
    FN123Factory(effort=eff2, species=pike, catcnt=2, biocnt=2)
    FN123Factory(effort=eff2, species=walleye, catcnt=3, biocnt=3)
    FN123Factory(effort=eff2, species=anyspc, catcnt=None)

    return project
