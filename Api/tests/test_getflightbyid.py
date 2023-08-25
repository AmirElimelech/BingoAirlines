from rest_framework.test import APITestCase
from rest_framework import status
from Bingo.models import Flights, Countries, Airline_Companies, Airport, Users, User_Roles
from django.utils import timezone
from datetime import timedelta
from Bingo.facades.facade_base import FacadeBase
from unittest.mock import patch




class GetFlightByIDAPITest(APITestCase):

    def setUp(self):
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")
        
        # Create a flight with a future timestamp
        self.flight = Flights.objects.create(airline_company_id=airline, flight_number="TA124", origin_airport=airport1, destination_airport=airport2, departure_time=timezone.now() + timedelta(hours=1), landing_time=timezone.now() + timedelta(hours=2), remaining_tickets=50)

    def test_valid_id(self):
        response = self.client.get(f"/Api/flights/{self.flight.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['flight_number'], "TA124")

    def test_invalid_id(self):
        response = self.client.get("/Api/flights/9999/")  # Assuming 9999 is an ID that doesn't exist
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # This tests an exception during the fetch operation, which is triggered by mocking the facade's method
    @patch.object(FacadeBase, 'get_flight_by_id', side_effect=Exception("Test Exception"))
    def test_exception_while_fetching(self, mock_method):
        response = self.client.get(f"/Api/flights/{self.flight.id}/")
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
