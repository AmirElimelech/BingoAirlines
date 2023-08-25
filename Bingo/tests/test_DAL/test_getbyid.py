
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone 
from Bingo.models import Flights, Countries, Airport, Airline_Companies, Users, User_Roles, DAL

class TestGetById(TestCase):

    @classmethod
    def setUpTestData(cls):
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=user_role)
        cls.airline = Airline_Companies.objects.create(iata_code="TA", name="TestAir", country_id=country, user_id=user)
        
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="STS", country_code="TC")
        departure_time = (timezone.now() + timedelta(days=1))
        landing_time = (timezone.now() + timedelta(days=2))
        cls.flight_instance = Flights.objects.create(
                                                        airline_company_id=cls.airline,
                                                        flight_number="TA123",
                                                        origin_airport=airport1,
                                                        destination_airport=airport2,
                                                        departure_time=timezone.now()+ timedelta(hours=1),
                                                        landing_time=timezone.now() + timedelta(hours=2),  
                                                        remaining_tickets=100  
                                                    )


    def test_get_by_id_valid(self):
        dal = DAL()
        flight = dal.get_by_id(Flights, self.flight_instance.id)
        self.assertEqual(flight, self.flight_instance)

    def test_get_by_id_invalid(self):
        dal = DAL()
        flight = dal.get_by_id(Flights, 9999)  # ID that doesn't exist
        self.assertIsNone(flight)



 