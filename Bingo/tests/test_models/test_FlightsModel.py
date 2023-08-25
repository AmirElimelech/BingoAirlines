from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles





class FlightsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create necessary dependencies
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        cls.airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        cls.airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")

    def test_create_and_retrieve_flight(self):
        flight = Flights.objects.create(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=100)
        retrieved_flight = Flights.objects.get(id=flight.id)
        self.assertEqual(retrieved_flight, flight)

    def test_flight_number_starts_with_iata_code(self):
        with self.assertRaises(ValidationError):
            flight = Flights(airline_company_id=self.airline, flight_number="WRONG123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=100)
            flight.full_clean()

    def test_flight_number_unique(self):
        Flights.objects.create(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=100)
        with self.assertRaises(ValidationError):
            duplicate_flight = Flights(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=3), landing_time=timezone.now()+timedelta(days=4), remaining_tickets=50)
            duplicate_flight.full_clean()

    def test_origin_and_destination_are_different(self):
        with self.assertRaises(ValidationError):
            flight = Flights(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport1, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=100)
            flight.full_clean()

    def test_departure_before_landing(self):
        with self.assertRaises(ValidationError):
            flight = Flights(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=2), landing_time=timezone.now()+timedelta(days=1), remaining_tickets=100)
            flight.full_clean()

    def test_departure_time_in_future(self):
        with self.assertRaises(ValidationError):
            flight = Flights(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()-timedelta(days=1), landing_time=timezone.now()+timedelta(days=1), remaining_tickets=100)
            flight.full_clean()

    def test_remaining_tickets_non_negative(self):
        with self.assertRaises(ValidationError):
            flight = Flights(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=-10)
            flight.full_clean()

    def test_string_representation(self):
        flight = Flights.objects.create(airline_company_id=self.airline, flight_number="TA123", origin_airport=self.airport1, destination_airport=self.airport2, departure_time=timezone.now()+timedelta(days=1), landing_time=timezone.now()+timedelta(days=2), remaining_tickets=100)
        self.assertEqual(str(flight), 'Flight TA123')
