from rest_framework.test import APITestCase
from rest_framework import status
from Bingo.models import Countries
from Bingo.facades.facade_base import FacadeBase
from unittest.mock import patch


class GetAllCountriesAPITest(APITestCase):

    def setUp(self):
        # Create some sample countries
        Countries.objects.create(name="TestCountry1", country_code="T1")
        Countries.objects.create(name="TestCountry2", country_code="T2")

    def test_countries_available(self):
        response = self.client.get("/Api/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Assuming you have default pagination settings, you should have a 'results' key in the response
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['name'], "TestCountry1")
        self.assertEqual(response.data['results'][1]['name'], "TestCountry2")

    def test_no_countries_available(self):
        # Delete all countries
        Countries.objects.all().delete()
        response = self.client.get("/Api/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    # This tests an exception during the fetch operation, which is triggered by mocking the facade's method
    @patch.object(FacadeBase, 'get_all_countries', side_effect=Exception("Test Exception"))
    def test_exception_while_fetching(self, mock_method):
        response = self.client.get("/Api/countries/")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
