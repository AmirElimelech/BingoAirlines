from datetime import timedelta
from django.test import TestCase
from django.utils import timezone 
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL


class TestGetAll(TestCase):

    @classmethod
    def setUpTestData(cls):
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")

        # Create multiple flights
        cls.flight1 = Flights.objects.create(
            airline_company_id=cls.airline,
            flight_number="TA123",
            origin_airport=airport1,
            destination_airport=airport2,
            departure_time=timezone.now() + timedelta(hours=1),
            landing_time=timezone.now() + timedelta(hours=2),
            remaining_tickets=100
        )
        
        cls.flight2 = Flights.objects.create(
            airline_company_id=cls.airline,
            flight_number="TA124",
            origin_airport=airport1,
            destination_airport=airport2,
            departure_time=timezone.now() + timedelta(hours=3),
            landing_time=timezone.now() + timedelta(hours=4),
            remaining_tickets=80
        )

    def test_get_all(self):
        dal = DAL()
        all_flights = dal.get_all(Flights)
        self.assertIn(self.flight1, all_flights)
        self.assertIn(self.flight2, all_flights)
        self.assertEqual(len(all_flights), 2)
