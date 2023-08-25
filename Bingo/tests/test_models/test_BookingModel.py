from django.test import TestCase
from django.core.exceptions import ValidationError
from Bingo.models import Users, User_Roles, Customers, Booking

class BookingModelTest(TestCase):
    
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
        cls.booking = Booking.objects.create(
            customer=customer,
            total_price=100.50
        )
        
    def test_create_and_retrieve_booking(self):
        # Test creation
        self.assertEqual(Booking.objects.count(), 1)
        
        # Test retrieval
        retrieved_booking = Booking.objects.first()
        self.assertEqual(retrieved_booking, self.booking)

    def test_total_price_validation(self):
        # Test negative total_price
        self.booking.total_price = -10.50
        with self.assertRaises(ValidationError):
            self.booking.full_clean()
        
    def test_string_representation(self):
        self.assertEqual(str(self.booking), f'Booking {self.booking.id} for Customer {self.booking.customer_id}')
