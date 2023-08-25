from datetime import timedelta
from django.test import TestCase
from django.utils import timezone 
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL


# Class method to set up test data before running the tests
class TestAdd(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creating a test country
        cls.country = Countries.objects.create(name="TestCountry", country_code="TC")
        # Creating a test user role
        cls.user_role = User_Roles.objects.create(role_name="Admin")
        # Creating a test user associated with the above role
        cls.user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=cls.user_role)
        # Creating a test airline company associated with the created country and user
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=cls.country, user_id=cls.user)\
        # Creating two test airports
        cls.airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        cls.airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")


    # Test case to validate the addition functionality
    def test_add_valid(self):
        # Creating an instance of DAL (Data Access Layer)
        dal = DAL()

        # Preparing test flight data
        flight_data = {
            "airline_company_id": self.airline,
            "flight_number": "TA125",
            "origin_airport": self.airport1,
            "destination_airport": self.airport2,
            "departure_time": timezone.now() + timedelta(hours=1),
            "landing_time": timezone.now() + timedelta(hours=2),
            "remaining_tickets": 75
        }

        # Calling the add method to add the flight
        created_flight = dal.add(Flights, **flight_data)
        # Asserting that the created flight is not None
        self.assertIsNotNone(created_flight)
        # Asserting that the flight number of the created flight is as expected
        self.assertEqual(created_flight.flight_number, "TA125")
        # Asserting that the created flight is present in the database
        self.assertTrue(Flights.objects.filter(flight_number="TA125").exists())
