from django.test import TestCase
from Bingo.models import  Users, User_Roles , Customers 
from django.core.exceptions import ValidationError

class CustomersModelTest(TestCase):

        @classmethod
        def setUpTestData(cls):
            # Creating a user for the ForeignKey relation
            cls.user = Users.objects.create(id="123456789", username="testuser", password="Pass@1234", email="test@bingo.com", user_role=User_Roles.objects.create(role_name="Customer"))

        def test_create_customer(self):
            customer = Customers.objects.create(first_name="John", last_name="Doe", address="123 Test St", phone_no="0501234567", credit_card_no="1234567812345678", user_id=self.user)
            self.assertEqual(customer.first_name, "John")

        def test_phone_number_valid(self):
            valid_numbers = ["0501234567", "+972501234567", "03-1234567", "+1234567890"]
            for number in valid_numbers:
                with self.subTest(phone_no=number):
                    customer = Customers(first_name="John", last_name="Doe", address="123 Test St", phone_no=number, credit_card_no="1234567812345678", user_id=self.user)
                    # This should not raise any errors
                    customer.full_clean()

        def test_phone_number_invalid(self):
            invalid_numbers = ["0501234", "972501234567", "03-12345", "1234567890"]
            for number in invalid_numbers:
                with self.subTest(phone_no=number):
                    customer = Customers(first_name="John", last_name="Doe", address="123 Test St", phone_no=number, credit_card_no="1234567812345678", user_id=self.user)
                    with self.assertRaises(ValidationError):
                        customer.full_clean()

        
        def test_image_url_property(self):
            customer = Customers.objects.create(first_name="John", last_name="Doe", address="123 Test St", phone_no="0501234567", credit_card_no="1234567812345678", user_id=self.user)
            self.assertIn("/users/defaultuser.png", customer.image_url)

        def test_str_method(self):
            customer = Customers.objects.create(first_name="John", last_name="Doe", address="123 Test St", phone_no="0501234567", credit_card_no="1234567812345678", user_id=self.user)
            self.assertEqual(str(customer), "John Doe")