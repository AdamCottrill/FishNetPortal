"""=============================================================
~/fn_portal/tests/integraion_tests/test_project_detail.py
 Created: 25 May 2020 09:44:52

 DESCRIPTION:

This file contains a number of tests to ensure that the project detail
 page renders as expected, uses the correct template and contains all
 of the required elements. If there are optional elements, they will
 be tested in both states.

 The project detail should:

  + use the correct template

  + contain the project code

  + contain the project name

  + contain the total number of net sets

  + contain the total catch count

  + contain a table with the total catch count by species

  + contain a table the the nets sets and their basic information

  + report the gear used in the project, including links to the gear
    detail page.

 A. Cottrill
=============================================================

"""


import pytest

from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed, assertContains, assertNotContains

from ..fixtures import project


@pytest.mark.django_db
def test_project_detail_uses_correct_template(client, project):
    """The project detail page should be rendered using 'fn_portal/project_detail.html'
    """

    url = reverse("fn_portal:project_detail", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "fn_portal/project_detail.html")


@pytest.mark.django_db
def test_project_detail_renders_project_name_and_code(client, project):
    """The project detail page should include a heading with the project
    name and project code

    """

    url = reverse("fn_portal:project_detail", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200

    expected = "<h2>{}({})</h2>".format(project.prj_nm.title(), project.prj_cd)
    assertContains(response, expected, html=True)


@pytest.mark.django_db
def test_project_detail_net_set_summary_table(client, project):
    """The project detail page should include a table will the basic
    informaion of each net set, including the total catch.

    """

    url = reverse("fn_portal:project_detail", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200

    sample_link = '<td><a href="{}">{}</a></td>'

    for sample in project.samples.all():
        expected = sample_link.format(sample.get_absolute_url(), sample.sam)
        assertContains(response, expected, html=True)
        assertContains(response, "<td>{}</td>".format(sample.gr), html=True)
        assertContains(response, "<td>{:.2f}</td>".format(sample.effdur), html=True)
        assertContains(response, "<td>{:.2f}</td>".format(sample.sidep), html=True)
        assertContains(
            response, "<td>{}</td>".format(sample.total_catch()["total"]), html=True
        )


@pytest.mark.django_db
def test_project_detail_catch_count_summary_table(client, project):
    """The project detail page should inlcude a table with the total catch
    and bio-smple catch by by species.  If the biosamples count is 0,
    the speceis name should just be text, if there are samples, there
    should be a link to the detail page.

    """
    url = reverse("fn_portal:project_detail", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200

    item_link = '<td><a href="{}">{} ({})</a></td>'

    for item in project.catch_counts():
        if item["biocnts"] > 0:
            url = reverse(
                "fn_portal:project_spc_biodata",
                kwargs={"slug": project.slug, "spc": item["spc"]},
            )
            expected = item_link.format(url, item["species"], item["spc"])
            assertContains(response, expected, html=True)
        else:
            assertNotContains(response, url, html=True)
            expected = "{} ({})".format(item["species"], item["spc"])
            assertContains(response, expected, html=True)

        assertContains(response, "<td>{}</td>".format(item["catcnts"]), html=True)
        assertContains(response, "<td>{}</td>".format(item["biocnts"]), html=True)


@pytest.mark.django_db
def test_project_detail_gear_list(client, project):
    """The project detail page should include a page listing the gears
    used in the project and links to details pages for those gears.

    """

    url = reverse("fn_portal:project_detail", kwargs={"slug": project.slug})
    response = client.get(url)
    assert response.status_code == 200

    gear_link = '<li><a href="{}">{}</a></li>'

    for gear_code in project.get_121_gear_codes():
        url = reverse("fn_portal:gear_detail", kwargs={"gear_code": gear_code})
        expected = gear_link.format(url, gear_code)
        assertContains(response, expected, html=True)
