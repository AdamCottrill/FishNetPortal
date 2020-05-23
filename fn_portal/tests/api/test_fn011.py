import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from fn_portal.tests.factories import FN011Factory, LakeFactory
from ..user_factory import UserFactory


class TestFN011List(APITestCase):
    @pytest.mark.django_db
    def setUp(self):

        homer = UserFactory(first_name="Homer", last_name="Simpson")
        bart = UserFactory(first_name="Bart", last_name="Simpson")
        huron = LakeFactory(lake_name="Huron", abbrev="HU")
        superior = LakeFactory(lake_name="Superior", abbrev="SU")

        self.project1 = FN011Factory(
            prj_cd="LHA_IA00_123", prj_nm="Homers Project", prj_ldr=homer, lake=huron
        )
        self.project2 = FN011Factory(prj_cd="LHA_IA05_999")
        self.project3 = FN011Factory(prj_cd="LSA_IA10_123", lake=superior)
        self.project4 = FN011Factory(prj_cd="LHA_IA02_123")
        self.project5 = FN011Factory(prj_cd="LHA_IA15_002", prj_ldr=bart)

    @pytest.mark.django_db
    def test_can_get_project_list(self):
        """Verify that all of our projects appear in our project list."""

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(len(results), 5)

    @pytest.mark.django_db
    def test_can_get_project_detail(self):
        """If we pass in a project code, we should see the corresponding project
        details"""

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"prj_cd": "LHA_IA00_123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("response.data={}".format(response.data))

        returned = response.data["results"][0]

        prj_ldr_dict = {
            "username": "simpsonho",
            "first_name": "Homer",
            "last_name": "Simpson",
        }

        self.assertEqual(returned["prj_cd"], "LHA_IA00_123")
        self.assertEqual(returned["prj_nm"], "Homers Project")
        self.assertEqual(returned["prj_ldr"], prj_ldr_dict)

    @pytest.mark.django_db
    def test_fn011_year_filter(self):
        "verify that we can filter by a single year."

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"year": 2002})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0].get("prj_cd"), "LHA_IA02_123")

    @pytest.mark.django_db
    def test_fn011_first_year_filter(self):
        """If we pass in just the first year, then all projects after
        that should be returned."""

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"first_year": 2005})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(len(results), 3)
        returned = [x["prj_cd"] for x in results]

        shouldbe = ["LHA_IA05_999", "LSA_IA10_123", "LHA_IA15_002"]

        for prj in shouldbe:
            self.assertIn(prj, returned)

    @pytest.mark.django_db
    def test_fn011_last_year_filter(self):
        """If we pass in just the last year, then all projects before
        that should be returned."""

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"last_year": 2002})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(len(results), 2)
        returned = [x["prj_cd"] for x in results]
        shouldbe = ["LHA_IA00_123", "LHA_IA02_123"]
        for prj in shouldbe:
            self.assertIn(prj, returned)

    @pytest.mark.django_db
    def test_fn011_between_years_filter(self):
        """Verify that we can filter projects based on the first and last years
        of a range."""

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"first_year": 2002, "last_year": 2010})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(len(results), 3)

        returned = [x["prj_cd"] for x in results]

        shouldbe = ["LHA_IA02_123", "LHA_IA05_999", "LSA_IA10_123"]

        for prj in shouldbe:
            self.assertIn(prj, returned)

    @pytest.mark.django_db
    def test_fn011_lake_filter(self):
        "Verify that we can filter projects based on the lake abbrevation"

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"lake": "SU"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("prj_cd"), "LSA_IA10_123")

    @pytest.mark.django_db
    def test_fn011_project_lead_filter(self):
        "Verify that we can filter projects based on the project leads username"
        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"prj_ldr": "simpsonba"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("prj_cd"), "LHA_IA15_002")

    @pytest.mark.django_db
    def test_fn011_project_suffix_filter(self):
        "Verify that we can filter projects based on the project suffix"

        url = reverse("fn_portal_api:fn011-list")
        response = self.client.get(url, {"suffix": "999"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].get("prj_cd"), "LHA_IA05_999")
