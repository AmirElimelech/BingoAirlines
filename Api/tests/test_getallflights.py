from django.test import TestCase, Client
from rest_framework import status
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles
from django.utils import timezone
from datetime import timedelta

class GetAllFlightsAPITest(TestCase):

    def setUp(self):
        self.client = Client()
        
        # Setting up necessary database entries
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")
        Flights.objects.create(airline_company_id=airline, flight_number="TA124", origin_airport=airport1, destination_airport=airport2, departure_time=timezone.now() + timedelta(hours=1), landing_time=timezone.now() + timedelta(hours=3), remaining_tickets=50)

    def test_get_all_flights_valid(self):
        response = self.client.get('/Api/flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) > 0) # Ensure there's at least one flight in the response.

    def test_get_all_flights_empty(self):
        # Delete all flights
        Flights.objects.all().delete()
        
        response = self.client.get('/Api/flights/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)  # Ensure no flights in the response.
