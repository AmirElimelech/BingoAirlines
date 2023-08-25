import logging
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone 
from Bingo.models import scheduler
from unittest.mock import patch , Mock
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL






test_logger = logging.getLogger('testlogger')


class TestAddAll(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.country = Countries.objects.create(name="TestCountry", country_code="TC")
        cls.user_role = User_Roles.objects.create(role_name="Admin")
        cls.user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=cls.user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=cls.country, user_id=cls.user)
        cls.airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        cls.airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")



    @patch('Bingo.models.scheduler.add_job', Mock())
    def test_add_all_valid(self):
        try:
            scheduler.remove_all_jobs()
            dal = DAL()
            flights_data = [
                {
                    "airline_company_id": self.airline,
                    "flight_number": "TA124",
                    "origin_airport": self.airport1,
                    "destination_airport": self.airport2,
                    "departure_time": timezone.now() + timedelta(hours=3),
                    "landing_time": timezone.now() + timedelta(hours=4),
                    "remaining_tickets": 80
                },
                {
                    "airline_company_id": self.airline,
                    "flight_number": "TA125",
                    "origin_airport": self.airport1,
                    "destination_airport": self.airport2,
                    "departure_time": timezone.now() + timedelta(hours=5),
                    "landing_time": timezone.now() + timedelta(hours=6),
                    "remaining_tickets": 90
                }
            ]
            created_flights = dal.add_all(Flights, flights_data)
            self.assertEqual(len(created_flights), 2)
            self.assertTrue(Flights.objects.filter(flight_number="TA124").exists())
            self.assertTrue(Flights.objects.filter(flight_number="TA125").exists())

            test_logger.info(f"TestAddAll - test_add_all_valid: Success")

        except Exception as e:
            # Logging errors
            test_logger.error(f"TestAddAll - test_add_all_valid: Error - {e}")
            raise  # Re-raise the exception to ensure the test fails
