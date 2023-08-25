from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from Bingo.models import Users, User_Roles, Customers, Booking, Flights, Airline_Companies, Countries, Airport, Tickets



class TicketsModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        # Create necessary dependencies
        user_role = User_Roles.objects.create(role_name="Admin")
        user = Users.objects.create(
            id="123456789", 
            username="testuser", 
            password="Pass@1234", 
            email="test@bingo.com", 
            user_role=user_role
        )
        customer = Customers.objects.create(
            first_name="John",
            last_name="Doe",
            address="123 Test St.",
            phone_no="0501234567",
            credit_card_no="1234567812345678",
            user_id=user
        )
        booking = Booking.objects.create(
            customer=customer,
            total_price=100.50
        )
        country = Countries.objects.create(name="TestCountry", country_code="TC")
        airline_company = Airline_Companies.objects.create(
            iata_code="TC",
            name="TestAirline",
            country_id=country,
            user_id=user
        )
        airport1 = Airport.objects.create(name="Test Airport 1", iata_code="TST", country_code="TC")
        airport2 = Airport.objects.create(name="Test Airport 2", iata_code="TS2", country_code="TC")
        future_date = timezone.now() + timezone.timedelta(days=1)
        flight = Flights.objects.create(
            airline_company_id=airline_company,
            flight_number="TCTEST01",
            origin_airport=airport1,
            destination_airport=airport2,
            departure_time=future_date,
            landing_time=future_date + timezone.timedelta(hours=2),
            remaining_tickets=50
        )
        cls.ticket = Tickets.objects.create(
            flight_number_ref=flight,
            customer_id=customer,
            Booking=booking,
            currency="USD",
            cabin="ECONOMY",
            adult_traveler_count=2,
            child_traveler_count=3
        )
        
    def test_create_and_retrieve_ticket(self):
        # Test creation
        self.assertEqual(Tickets.objects.count(), 1)
        
        # Test retrieval
        retrieved_ticket = Tickets.objects.first()
        self.assertEqual(retrieved_ticket, self.ticket)

    def test_traveler_count_validation(self):
        # Test total traveler count exceeding 9
        self.ticket.adult_traveler_count = 5
        self.ticket.child_traveler_count = 5
        with self.assertRaises(ValidationError):
            self.ticket.full_clean()
        
    def test_currency_and_cabin_validation(self):
        # Test invalid currency
        self.ticket.currency = "INVALID"
        with self.assertRaises(ValidationError):
            self.ticket.full_clean()
        
        # Test invalid cabin
        self.ticket.currency = "USD"  # Reset to valid value
        self.ticket.cabin = "INVALID"
        with self.assertRaises(ValidationError):
            self.ticket.full_clean()

    def test_past_flight_validation(self):
        # Modify flight's departure_time to a past time
        past_date = timezone.now() - timezone.timedelta(days=1)
        self.ticket.flight_number_ref.departure_time = past_date
        with self.assertRaises(ValidationError):
            self.ticket.full_clean()

    def test_string_representation(self):
        self.assertEqual(str(self.ticket), f'Ticket {self.ticket.id}')
