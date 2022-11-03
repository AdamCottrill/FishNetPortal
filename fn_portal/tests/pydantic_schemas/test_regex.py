import pytest
import re

from fn_portal.data_upload.schemas.regular_expressions import (
    SPCMRK_REGEX,
    AGEST_REGEX,
    FDSAM_REGEX,
)

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


valid_agest = [
    "0",
    "0",
    "1",
    "1A",
    "2",
    "23",
    "23A",
    "2A",
    "247A",
    "45",
    "4A",
    "4ABF",
    "5",
    "A",
]


invalid_agest = [
    "",
    " ",
    "01",
    "K0",
    "\\",
    "00",
    "10",
    "20",
    "50",
    "A0",
    "B0",
    "D0",
    "X0",
]


@pytest.mark.parametrize("value", valid_agest)
def test_valid_agest(value):
    """Our spcmark regular expression should match all of our valid
    spcmarks."""

    assert re.match(AGEST_REGEX, value) is not None


@pytest.mark.parametrize("value", invalid_agest)
def test_invalid_agest(value):
    """our regular expression should not match spcmark values that are not
    valid"""
    assert re.match(AGEST_REGEX, value) is None


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
