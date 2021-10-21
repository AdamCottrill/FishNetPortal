import pytest


from ..api.utils import check_distinct_seasons


seasons_list = [
    (
        [],
        True,
    ),
    (
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-08-10"},
        ],
        True,
    ),
    (
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-08-10"},
            {"ssn_date0": "2021-09-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": "2021-10-01", "ssn_date1": "2021-10-10"},
        ],
        True,
    ),
    (
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-08-10"},
            {"ssn_date0": "2021-09-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": "2021-10-01", "ssn_date1": None},
        ],
        True,
    ),
    (
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-08-10"},
            {"ssn_date0": "2021-09-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": None, "ssn_date1": "2021-10-10"},
        ],
        True,
    ),
    (
        # overlapping
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": "2021-09-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": "2021-10-01", "ssn_date1": "2021-10-10"},
        ],
        False,
    ),
    (
        # overlapping by one day
        [
            {"ssn_date0": "2021-08-01", "ssn_date1": "2021-09-10"},
            {"ssn_date0": "2021-09-01", "ssn_date1": "2021-10-01"},
            {"ssn_date0": "2021-10-01", "ssn_date1": "2021-10-10"},
        ],
        False,
    ),
]


@pytest.mark.parametrize("seasons,expectation", seasons_list)
def test_check_distinct_seasons(seasons, expectation):
    """the check_distinct_seasons function verifies that seasons do not
    overlap - it should return true if the values are disticnt(valid)
    and do not overlap, but should returns false if the season are not
    distict and share some dates.  This test accepts and array of
    season dictinaryies and the expected return value from
    check_distict_seasons.

    """

    assert check_distinct_seasons(seasons) is expectation
