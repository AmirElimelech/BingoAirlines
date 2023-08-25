from datetime import timedelta
from django.test import TestCase
from django.utils import timezone 
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL



class TestUpdate(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.country = Countries.objects.create(name="TestCountry", country_code="TC")
        cls.user_role = User_Roles.objects.create(role_name="Admin")
        cls.user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=cls.user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=cls.country, user_id=cls.user)
        cls.airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        cls.airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")
        cls.flight_instance = Flights.objects.create(
                                                        airline_company_id=cls.airline,
                                                        flight_number="TA123",
                                                        origin_airport=cls.airport1,
                                                        destination_airport=cls.airport2,
                                                        departure_time=timezone.now() + timedelta(hours=1),
                                                        landing_time=timezone.now() + timedelta(hours=2),
                                                        remaining_tickets=100
                                                    )

    def test_update_valid(self):
        dal = DAL()
        updated_attrs = {
            "flight_number": "TA126",
            "remaining_tickets": 50
        }
        updated_flight = dal.update(self.flight_instance, **updated_attrs)
        self.assertIsNotNone(updated_flight)
        self.assertEqual(updated_flight.flight_number, "TA126")
        self.assertEqual(updated_flight.remaining_tickets, 50)
        self.assertTrue(Flights.objects.filter(flight_number="TA126", remaining_tickets=50).exists())
