
from datetime import timedelta
from unittest.mock import patch
from django.test import TestCase
from django.utils import timezone
from Bingo.models import Users, User_Roles, Countries, Airline_Companies, Airport, Flights, DAL

class TestGetFlightsByParameters(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create necessary dependencies
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")

        # Create a flight for testing
        departure_time = (timezone.now() + timedelta(days=1))
        landing_time = (timezone.now() + timedelta(days=2))
        created_flight = Flights.objects.create(airline_company_id=airline, flight_number="TA123", origin_airport=airport1, destination_airport=airport2, departure_time=departure_time, landing_time=landing_time, remaining_tickets=100)

        # Print the created flight details for debugging
        print(created_flight.origin_airport, created_flight.destination_airport, created_flight.departure_time)
        
    @patch('Bingo.utils.tasks.download_airline_logo')
    def test_get_flights_by_parameters(self, mocked_download):
        # Mocking the download so it doesn't actually run
        mocked_download.return_value = None
        
        dal = DAL()
        
        # Defining the parameters for the flight search
        parameters = {
            'origin_airport': 'TST',
            'destination_airport': 'STS',
            'departure_date': (timezone.now() + timedelta(days=1)).date().strftime('%Y-%m-%d')
        }
        
        flights = dal.get_flights_by_parameters(parameters)
        
        self.assertEqual(len(flights), 1)

