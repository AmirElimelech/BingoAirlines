from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from Bingo.models import Countries
from Bingo.facades.facade_base import FacadeBase
from Api.serializers import CountriesSerializer


class GetCountryByIdAPITest(APITestCase):

    def setUp(self):
        self.country = Countries.objects.create(name="Testland", country_code="TL")

    @patch.object(FacadeBase, 'get_country_by_id')
    def test_valid_country_code_exists(self, mock_get_country):
        mock_get_country.return_value = self.country
        response = self.client.get('/Api/countries/TL/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, CountriesSerializer(self.country).data)

    @patch.object(FacadeBase, 'get_country_by_id')
    def test_valid_country_code_not_exists(self, mock_get_country):
        mock_get_country.return_value = None
        response = self.client.get('/Api/countries/XX/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_country_code(self):
        response = self.client.get('/Api/countries/123/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_country_code_2(self):
        response = self.client.get('/Api/countries/T1/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(FacadeBase, 'get_country_by_id')
    def test_exception_while_fetching(self, mock_get_country):
        mock_get_country.side_effect = Exception("DB error")
        response = self.client.get('/Api/countries/TL/')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
