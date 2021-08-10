"""=============================================================
 c:/Users/COTTRILLAD/1work/Python/djcode/apps/fn_portal/fn_portal/tests/integraion_tests/test_sample_detail.py
 Created: 25 May 2020 14:29:10

 DESCRIPTION:

  The sample detail page uses the 'fn_portal/sample_detail.html'
  template and should include basic inforamtion about the net set
  (sample number. set data and time. lift data and time, effort
  duration, orientation and set depth), as well as a summary of the
  catch and bio-samples by by speceies.

 A. Cottrill
=============================================================

"""


import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains, assertNotContains, assertTemplateUsed

from ..fixtures import project


@pytest.mark.django_db
def test_sample_detail_uses_correct_template(client, project):
    """The sample detail page should be rendered using 'fn_portal/sample_detail.html'"""

    sample = project.samples.first()
    url = reverse(
        "fn_portal:sample_detail", kwargs={"slug": project.slug, "sam": sample.sam}
    )
    response = client.get(url)
    assert response.status_code == 200
    assertTemplateUsed(response, "fn_portal/sample_detail.html")


@pytest.mark.django_db
def test_sample_detail_renders_headings(client, project):
    """The sample detail page should gontain heading that report the
    proejct code and sample number, and the totlta catch for this
    sample.
    """

    sample = project.samples.first()
    url = reverse(
        "fn_portal:sample_detail", kwargs={"slug": project.slug, "sam": sample.sam}
    )
    response = client.get(url)
    assert response.status_code == 200

    expected = '<h2>Sample Details: {} from <a href="{}">{}</a></h2>'
    assertContains(
        response,
        expected.format(sample.sam, project.get_absolute_url(), project.prj_cd),
        html=True,
    )

    expected = "<h3>Catch Composition ({} fish in total)</h3>"
    assertContains(response, expected.format(sample.total_catch()["total"]), html=True)


@pytest.mark.django_db
def test_sample_detail_renders_net_attributes(client, project):
    """should include basic inforamtion about the net set
    (sample number. set data and time. lift data and time, effort
    duration, orientation and set depth),
    """

    # sam 1 has both dates and times for set and lift times
    sample = project.samples.get(sam="1")
    url = reverse(
        "fn_portal:sample_detail", kwargs={"slug": project.slug, "sam": sample.sam}
    )
    response = client.get(url)
    assert response.status_code == 200

    assertContains(response, "<td>{}</td>".format(sample.sam), html=True)
    assertContains(
        response,
        "<td>{} at {}</td>".format(
            sample.effdt0.strftime("%B %d, %Y"), sample.efftm0.strftime("%H:%M")
        ),
        html=True,
    )
    assertContains(
        response,
        "<td>{} at {}</td>".format(
            sample.effdt1.strftime("%B %d, %Y"), sample.efftm1.strftime("%H:%M")
        ),
        html=True,
    )
    assertContains(response, "<td>{}</td>".format(sample.mode.gear.gr_code), html=True)
    assertContains(response, "<td>{}</td>".format(sample.mode.orient), html=True)
    assertContains(response, "<td>{:.2f}</td>".format(sample.effdur), html=True)
    assertContains(response, "<td>{:.1f}</td>".format(sample.sidep), html=True)


@pytest.mark.django_db
def test_sample_detail_renders_dates_without_time(client, project):
    """The set and lift time contain contiational logic to report the time
    when it is available, and skip it if is is not. the Second sample
    in our fixture does not have any set or lift time and should bre
    presented in a simpler fashion.

    """

    # sam 1 has both dates and times for set and lift times
    sample = project.samples.get(sam="2")
    url = reverse(
        "fn_portal:sample_detail", kwargs={"slug": project.slug, "sam": sample.sam}
    )
    response = client.get(url)
    assert response.status_code == 200

    assertContains(
        response, "<td>{}</td>".format(sample.effdt1.strftime("%B %d, %Y")), html=True
    )
    assertContains(
        response, "<td>{}</td>".format(sample.effdt1.strftime("%B %d, %Y")), html=True
    )


@pytest.mark.django_db
def test_sample_detail_renders_catch_counts(client, project):
    """The sample detail page should inlcude a table with the total catch
    and bio-smple catch by by species.
    """

    sample = project.samples.first()
    url = reverse(
        "fn_portal:sample_detail", kwargs={"slug": project.slug, "sam": sample.sam}
    )
    response = client.get(url)
    assert response.status_code == 200

    for item in sample.catch_counts():
        expected = "<td>{} ({})</td>".format(item["species"], item["spc"])
        assertContains(response, expected, html=True)
        assertContains(response, "<td>{}</td>".format(item["catcnts"]), html=True)
        assertContains(response, "<td>{}</td>".format(item["biocnts"]), html=True)
