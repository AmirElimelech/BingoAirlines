from django.test import TestCase
from Bingo.models import Users, User_Roles 
from django.core.exceptions import ValidationError

class UsersModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Setting up a user role for the user
        cls.user_role = User_Roles.objects.create(role_name="Customer")
        
        # Creating a test user
        cls.user = Users.objects.create(id='123456789', username='testuser', password='Test@12345', 
                                        email='testuser@gmail.com', user_role=cls.user_role)

    def test_user_creation(self):
        """Test if the user is saved correctly."""
        saved_user = Users.objects.first()
        self.assertEqual(saved_user, self.user)
        self.assertEqual(saved_user.username, 'testuser')

    def test_id_length(self):
        """Test the ID length requirement."""
        with self.assertRaises(ValidationError):
            user = Users(id='12345678', username='testuser2', password='Test@12345', 
                         email='testuser2@gmail.com', user_role=self.user_role)
            user.full_clean()

    def test_password_strength(self):
        """Test password strength requirement."""
        with self.assertRaises(ValidationError):
            user = Users(id='987654321', username='testuser3', password='test12345', 
                         email='testuser3@gmail.com', user_role=self.user_role)
            user.full_clean()

    def test_email_field(self):
        """Test the email field of the user."""
        saved_user = Users.objects.first()
        self.assertEqual(saved_user.email, 'testuser@gmail.com')

    def test_image_url(self):
        """Test the image_url property method."""
        saved_user = Users.objects.first()
        self.assertIn('/users/', saved_user.image_url)

    def test_is_authenticated(self):
        """Test the is_authenticated property."""
        saved_user = Users.objects.first()
        self.assertTrue(saved_user.is_authenticated)
