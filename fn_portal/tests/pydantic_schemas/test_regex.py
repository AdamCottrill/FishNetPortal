import pytest
import re

from fn_portal.data_upload.schemas.FN012 import SPCMRK_REGEX, AGEDEC_REGEX, FDSAM_REGEX

valid_spcmrk = ["0", "10", "11", "12", "20", "21", "30", "31", "32"]

invalid_spcmrk = [
    "",
    "1",
    "2",
    "3",
    "00",
    "01",
]


@pytest.mark.parametrize("value", valid_spcmrk)
def test_valid_spcmrk(value):
    """Our spcmark regular expression should match all of our valid
    spcmarks."""

    assert re.match(SPCMRK_REGEX, value) is not None


@pytest.mark.parametrize("value", invalid_spcmrk)
def test_invalid_spcmrk(value):
    """our regular expression should not match spcmark values that are not
    valid"""
    assert re.match(SPCMRK_REGEX, value) is None


valid_agedec = [
    "0",
    "00",
    "10",
    "20",
    "21",
    "50",
    "A0",
    "A1",
    "B0",
    "D0",
    "X0",
    "X1",
]

invalid_agedec = [
    "",
    "01",
    "02",
    "22",
    "2",
    "KK",
    "K0",
    "K1",
    "X",
    "\\",
]


@pytest.mark.parametrize("value", valid_agedec)
def test_valid_agedec(value):
    """Our spcmark regular expression should match all of our valid
    spcmarks."""

    assert re.match(AGEDEC_REGEX, value) is not None


@pytest.mark.parametrize("value", invalid_agedec)
def test_invalid_agedec(value):
    """our regular expression should not match spcmark values that are not
    valid"""
    assert re.match(AGEDEC_REGEX, value) is None


valid_fdsam = ["0", "11", "12", "13", "21", "22", "23"]

invalid_fdsam = [
    "",
    "1",
    "2",
    "00",
    "01",
    "02",
    "20",
]


@pytest.mark.parametrize("value", valid_fdsam)
def test_valid_fdsam(value):
    """Our spcmark regular expression should match all of our valid
    spcmarks."""

    assert re.match(FDSAM_REGEX, value) is not None


@pytest.mark.parametrize("value", invalid_fdsam)
def test_invalid_fdsam(value):
    """our regular expression should not match spcmark values that are not
    valid"""
    assert re.match(FDSAM_REGEX, value) is None
