from django.test import TestCase
from Bingo.models import Airport
from django.core.exceptions import ValidationError


class AirportModelTest(TestCase):

    def setUp(self):
        self.valid_airport_data = {
            'name': 'John F. Kennedy International Airport',
            'iata_code': 'JFK',
            'country_code': 'US'
        }

    def test_string_representation(self):
        airport = Airport(**self.valid_airport_data)
        self.assertEqual(str(airport), self.valid_airport_data['name'])

    def test_save_and_retrieve_airport(self):
        airport = Airport(**self.valid_airport_data)
        airport.save()
        retrieved_airport = Airport.objects.get(iata_code='JFK')
        self.assertEqual(retrieved_airport, airport)

    def test_uppercase_iata_code(self):
        # Test with valid uppercase IATA code
        airport = Airport(**self.valid_airport_data)
        airport.clean()

        # Test with invalid lowercase IATA code
        invalid_airport_data = self.valid_airport_data.copy()
        invalid_airport_data['iata_code'] = 'jfk'
        airport = Airport(**invalid_airport_data)
        with self.assertRaises(ValidationError):
            airport.clean()

    def test_save_method_calls_full_clean(self):
        invalid_airport_data = self.valid_airport_data.copy()
        invalid_airport_data['iata_code'] = 'jfk'
        airport = Airport(**invalid_airport_data)
        with self.assertRaises(ValidationError):
            airport.save()

    def test_country_code_length(self):
        # Create an airport with a country code of length not equal to 2
        airport = Airport(name="Test Airport", iata_code="TST", country_code="TEST")
        with self.assertRaises(ValidationError):
            airport.save()

