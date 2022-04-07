"""=============================================================
~/fn_portal/tests/integraion_tests/test_project_list.py
 Created: 23 May 2020 13:25:09

 DESCRIPTION:

  Tests to make sure that the project list renders as expected and
  contains all of the reqiured elements.

+ it should contain a list of projects, and present the year, project
code, project name, project lead and project source for each project.

+ it should contain a Refine by sidebar that contains panels for lake,
year, project code and project source.

+ each panel should include a hyperlink for each criteria and counts
of currently selected projects

+ the project list accepts filters for year, first year, last year,
project code, source and project list. When one of those filters are
selected, only projects that meet that criteri should be selected.  A
button to remove the filter should also be included in the response.


 A. Cottrill
=============================================================

"""


import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains

from ..fixtures import project_list


@pytest.mark.django_db
def test_project_list_renders(client, project_list):
    """The project list pages should contain the string "Welcome to fish
    net portal" and a table that includes a list of projects, and present
    the year, project code, project name, project lead and project source
    for each project.

    """

    url = reverse("fn_portal:project_list")
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "fn_portal/project_list.html")
    content = "<h2>Welcome to FishNet Portal</h2>"
    assertContains(response, content, html=True)

    # the view should contain all of our project codes, project titles, and project leads:

    prj_cds = [
        "LHA_IA19_000",
        "LHA_IA10_111",
        "LSA_IA15_222",
        "LHA_IA19_333",
        "LSA_IA10_444",
        "LHA_IA15_555",
    ]
    for item in prj_cds:
        assertContains(response, content)
    years = ["2010", "2015", "2019"]

    for item in years:
        assertContains(response, content)

    prj_ldrs = ["Barney Gumble", "Homer Simpson"]
    for item in prj_ldrs:
        assertContains(response, content)

    sources = ["Nearshore", "Offshore", "Smallfish"]
    for item in sources:
        assertContains(response, content)


# the filter test is parametertized to take a 4 element tuple containing:
# the filter key, filter value, expected project, excluded projects

filter_attrs = [
    (
        "year",
        2015,
        ["LHA_IA15_555", "LSA_IA15_222"],
        ["LSA_IA10_444", "LHA_IA10_111", "LHA_IA19_000", "LHA_IA19_333"],
    ),
    (
        "first_year",
        2015,
        ["LHA_IA15_555", "LSA_IA15_222", "LHA_IA19_000", "LHA_IA19_333"],
        ["LSA_IA10_444", "LHA_IA10_111"],
    ),
    (
        "last_year",
        2015,
        ["LSA_IA10_444", "LHA_IA10_111", "LHA_IA15_555", "LSA_IA15_222"],
        ["LHA_IA19_000", "LHA_IA19_333"],
    ),
    (
        "lake",
        "SU",
        ["LSA_IA10_444", "LSA_IA15_222"],
        ["LHA_IA19_000", "LHA_IA19_333", "LHA_IA10_111", "LHA_IA15_555"],
    ),
    (
        "source",
        "offshore",
        ["LSA_IA15_222", "LHA_IA19_333", "LSA_IA10_444", "LHA_IA19_666"],
        ["LHA_IA19_000", "LHA_IA10_111", "LHA_IA15_555"],
    ),
    (
        "prj_ldr",
        "simpsonho",
        ["LHA_IA19_000", "LHA_IA10_111", "LSA_IA15_222", "LHA_IA19_333"],
        ["LSA_IA10_444", "LHA_IA15_555", "LHA_IA19_666"],
    ),
    (
        "prj_cd__like",
        "LSA",
        ["LSA_IA15_222", "LSA_IA10_444"],
        [
            "LHA_IA19_000",
            "LHA_IA10_111",
            "LHA_IA19_333",
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
    ),
    (
        "prj_cd__like",
        "lsa",
        ["LSA_IA15_222", "LSA_IA10_444"],
        [
            "LHA_IA19_000",
            "LHA_IA10_111",
            "LHA_IA19_333",
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
    ),
    (
        "prj_cd",
        "LSA_IA15_222",
        ["LSA_IA15_222"],
        [
            "LHA_IA19_000",
            "LHA_IA10_111",
            "LHA_IA19_333",
            "LSA_IA10_444",
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
    ),
    # search should be case insensitive - all of these should return the same projects:
    (
        "search",
        "FindMe",
        ["LSA_IA10_444", "LHA_IA15_555", "LHA_IA19_666"],
        ["LHA_IA19_000", "LHA_IA10_111", "LSA_IA15_222", "LHA_IA19_333"],
    ),
    (
        "search",
        "findme",
        ["LSA_IA10_444", "LHA_IA15_555", "LHA_IA19_666"],
        ["LHA_IA19_000", "LHA_IA10_111", "LSA_IA15_222", "LHA_IA19_333"],
    ),
    (
        "search",
        "FINDME",
        ["LSA_IA10_444", "LHA_IA15_555", "LHA_IA19_666"],
        ["LHA_IA19_000", "LHA_IA10_111", "LSA_IA15_222", "LHA_IA19_333"],
    ),
    # search should work on project codes too:
    (
        "search",
        "LSA",
        ["LSA_IA15_222", "LSA_IA10_444"],
        [
            "LHA_IA19_000",
            "LHA_IA10_111",
            "LHA_IA19_333",
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
    ),
    (
        "status",
        "complete",
        [
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
        [
            "LHA_IA19_000",
            "LSA_IA15_222",
            "LHA_IA10_111",
            "LHA_IA19_333",
            "LSA_IA10_444",
        ],
    ),
    (
        "status",
        "validated,complete",
        [
            "LHA_IA19_333",
            "LSA_IA10_444",
            "LHA_IA15_555",
            "LHA_IA19_666",
        ],
        [
            "LHA_IA19_000",
            "LSA_IA15_222",
            "LHA_IA10_111",
        ],
    ),
]


@pytest.mark.parametrize("filter,value,expected,excluded", filter_attrs)
@pytest.mark.django_db
def test_project_list_filter(client, project_list, filter, value, expected, excluded):
    """this can be another parameterized test that accepts a filter and a
    list of project codes that are expected to appear in the response.
    """

    url = reverse("fn_portal:project_list")
    response = client.get(url + "?{}={}".format(filter, value))
    assert response.status_code == 200

    for item in expected:
        assertContains(response, item)
    for item in excluded:
        assertNotContains(response, item)


@pytest.mark.django_db
def test_project_list_no_projects(client, project_list):
    """If no project match the selected criteria, the repsonse should
    incude meaingful message.

    """
    url = reverse("fn_portal:project_list")
    response = client.get(url + "?search=foo-bar-baz")
    assert response.status_code == 200

    msg = "<h4>Sorry, no projects match that criteria.</h4>"
    assertContains(response, msg, html=True)


html = [
    ("<h5>Refine By:</h5>"),
    ('<div class="card-header">Lake</div>'),
    ('<div class="card-header">Years</div>'),
    ('<div class="card-header">Project Code</div>'),
    ('<div class="card-header">Project Source</div>'),
    ('<div class="card-header">Project Status</div>'),
]


@pytest.mark.parametrize("content", html)
@pytest.mark.django_db
def test_project_list_refine_by_sidebar(client, content):
    """The response should contain a "Refine By" sidebar that contains panels for lake,
    year, project code and project source.

    Each panel should include a hyperlink for each criteria and counts
    of currently selected projects
    """

    url = reverse("fn_portal:project_list")
    response = client.get(url)
    assert response.status_code == 200

    assertContains(response, content, html=True)


filter_buttons = [
    (
        "source",
        "smallfish",
        """<a class='btn btn-danger btn-sm btn-pill'
     href='/fn_portal/' role='button'>
     Source: Smallfish
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "year",
        "2015",
        """<a class='btn btn-success btn-sm btn-pill'
     href='/fn_portal/' role='button'>
     2015
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "first_year",
        "2015",
        """<a class='btn btn-success btn-sm btn-pill'
     href='/fn_portal/' role='button'>
     After 2015
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "last_year",
        "2015",
        """<a class='btn btn-success btn-sm btn-pill'
     href='/fn_portal/' role='button'>
     Before 2015
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "lake",
        "HU",
        """<a class='btn btn-primary btn-sm btn-pill'
     href='/fn_portal/' role='button'>
     Huron
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "prj_ldr",
        "simpsonho",
        """<a class='btn btn-secondary btn-sm btn-pill'
     href='/fn_portal/' role='button'>
        Run By simpsonho
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "search",
        "findme",
        """<a class='btn btn-info btn-sm btn-pill'
     href='/fn_portal/' role='button'>
        contains findme
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "prj_cd__like",
        "_123",
        """<a class='btn btn-warning btn-sm btn-pill'
     href='/fn_portal/' role='button'>
        Project Code like: _123
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
    (
        "status",
        "complete",
        """<a class='btn btn-primary btn-sm btn-pill'
     href='/fn_portal/' role='button'>
        Status: Complete
     <i class="fa fa-times-circle"></i>
     </a>""",
    ),
]


@pytest.mark.parametrize("filter, value, html", filter_buttons)
@pytest.mark.django_db
def test_project_list_remove_filter_buttons(client, project_list, filter, value, html):
    """- this should be a
    parmaterized test that accepts the filter and the expected
    buttons.
    """
    url = reverse("fn_portal:project_list")
    response = client.get(url + "?{}={}".format(filter, value))
    assert response.status_code == 200

    assertContains(response, html, html=True)

    # reset link should always appear if a filter is actve:
    reset_html = '<a class="pull-right" href="/fn_portal/">Clear Filters</a>'

    assertContains(response, reset_html, html=True)
