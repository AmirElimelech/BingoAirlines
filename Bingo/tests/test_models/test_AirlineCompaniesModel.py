
from PIL import Image
from io import BytesIO
from unittest.mock import patch
from django.test import TestCase
from Bingo.utils.scheduler import scheduler
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from Bingo.models import Users, User_Roles, Countries, Airline_Companies






class AirlineCompaniesModelTest(TestCase):
    
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
        country = Countries.objects.create(name="TestCountry", country_code="TC")

        image = Image.new('RGB', (100, 100))
        buf = BytesIO()
        image.save(buf, 'PNG')
        cls.image_file = SimpleUploadedFile("test_image.png", buf.getvalue(), content_type="image/png")

        cls.airline_company = Airline_Companies.objects.create(
            iata_code="TC",
            name="TestAirline",
            country_id=country,
            user_id=user,
            logo=cls.image_file
        )
        
    def test_create_and_retrieve_airline_company(self):
        # Test creation
        self.assertEqual(Airline_Companies.objects.count(), 1)
        
        # Test retrieval
        retrieved_ac = Airline_Companies.objects.first()
        self.assertEqual(retrieved_ac, self.airline_company)

    def test_iata_code_uppercase_validation(self):
        # Test lowercase iata_code
        self.airline_company.iata_code = "tc"
        with self.assertRaises(ValidationError):
            self.airline_company.full_clean()

    def test_string_representation(self):
        self.assertEqual(str(self.airline_company), "TestAirline")

    def test_logo_save_logic(self):
        self.airline_company.save()
        print("Saved Logo Name:", self.airline_company.logo.name)
        self.assertTrue(self.airline_company.logo.name.startswith('airline_logos/TC'))


    def test_no_logo_provided(self):
        # Ensure the logo is None before saving
        self.airline_company.logo = None

        # Mock the scheduler's add_job method
        with patch.object(scheduler, 'add_job', return_value=None) as mock_add_job:
            self.airline_company.save()
            
            # Check if the add_job method was called
            mock_add_job.assert_called_once()

        self.assertIsNone(self.airline_company.logo.name)



    @classmethod
    def tearDownClass(cls):
        # Close the image after tests
        cls.image_file.close()
        super().tearDownClass()
