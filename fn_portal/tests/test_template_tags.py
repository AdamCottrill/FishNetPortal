import pytest


from fn_portal.templatetags.fn_portal_tags import status_badge


badge_attrs = [
    ("nomatch", ["Nomatch", "bg-secondary", "fa-question-circle"]),
    (
        "archive",
        [
            "Archive",
            "bg-danger",
            "fa-exclamation-triangle",
        ],
    ),
    (
        "initiated",
        [
            "Initiated",
            "bg-warning",
            "fa-tasks",
        ],
    ),
    (
        "validated",
        [
            "Validated",
            "bg-info",
            "fa-check-circle",
        ],
    ),
    ("complete", ["Complete", "bg-success", "fa-lock"]),
]


@pytest.mark.parametrize("status,values", badge_attrs)
def test_status_badge_templatetag(status, values):
    """The status badge template tag accepts a status string and returns
    the html corresponding to a bootstrap 5 badge. The badge contains
    the capialized version of the status, and has a different color
    and icon depending on teh status. If an unknown status is passed
    in, it should be grey with a question mark.
    """

    html = status_badge(status)

    for item in values:
        assert item in html
