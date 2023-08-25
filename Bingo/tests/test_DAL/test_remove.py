
import logging
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from unittest.mock import Mock, patch
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL


logger = logging.getLogger('testlogger')

class TestRemove(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.country = Countries.objects.create(name="TestCountry", country_code="TC")
        cls.user_role = User_Roles.objects.create(role_name="Admin")
        cls.user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=cls.user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=cls.country, user_id=cls.user)
        cls.airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        cls.airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")

    @patch('Bingo.models.scheduler.add_job', Mock())
    def test_remove_valid(self):
        dal = DAL()
        flight = Flights.objects.create(
            airline_company_id=self.airline,
            flight_number="TA126",
            origin_airport=self.airport1,
            destination_airport=self.airport2,
            departure_time=timezone.now() + timedelta(hours=3),
            landing_time=timezone.now() + timedelta(hours=4),
            remaining_tickets=80
        )
        result = dal.remove(flight)
        self.assertTrue(result)
        self.assertFalse(Flights.objects.filter(flight_number="TA126").exists())
        logger.info("TestRemove - test_remove_valid: Success")

    @patch('Bingo.models.scheduler.add_job', Mock())
    @patch('Bingo.models.logger.error')
    def test_remove_invalid(self, mock_logger_error):
        dal = DAL()

        # Create a mock instance that doesn't exist in the database
        mock_instance = Mock(spec=Flights)
        mock_instance.delete.side_effect = Exception("Deletion error")

        result = dal.remove(mock_instance)
        self.assertIsNone(result)

        # Ensure the logger was called with the error message
        mock_logger_error.assert_called_once()
