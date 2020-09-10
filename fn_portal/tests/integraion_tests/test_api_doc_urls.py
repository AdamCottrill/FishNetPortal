"""=============================================================
~/fn_portal/tests/integraion_tests/test_api_doc_urls.py
 Created: 04 Sep 2020 16:39:53

 DESCRIPTION:

   A couple of simple integraion_tests to verify that the api
   documentation urls are available (status code 200)

 A. Cottrill
=============================================================

"""


import pytest
from django.urls import reverse

url_names = ["schema-swagger-ui", "schema-redoc"]


@pytest.mark.parametrize("url_name", url_names)
def test_api_doc_url(client, url_name):
    """Make sure we can load the api documentation endpoints.

    Arguments:
    - `client`:
    - `url`:
    """
    url = reverse("fn_portal:" + url_name)
    response = client.get(url)
    assert response.status_code == 200
