from django.test import TestCase
from Bingo.models import Administrators, Users, User_Roles

class AdministratorsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user_role = User_Roles.objects.create(role_name="Admin")
        cls.user = Users.objects.create(id="123456789", username="testadmin", password="Pass@1234", email="admin@bingo.com", user_role=user_role)

    def test_string_representation(self):
        admin = Administrators.objects.create(first_name="John", last_name="Admin", user_id=self.user)
        self.assertEqual(str(admin), "John Admin")

    def test_user_id_unique(self):
        admin = Administrators.objects.create(first_name="Jane", last_name="Doe", user_id=self.user)
        with self.assertRaises(Exception):
            # Trying to create another admin with the same user should raise an exception
            another_admin = Administrators.objects.create(first_name="Janet", last_name="Smith", user_id=self.user)

    def test_verbose_name_plural(self):
        self.assertEqual(Administrators._meta.verbose_name_plural, "Administrators")

    def test_create_and_retrieve_administrator(self):
        admin = Administrators.objects.create(first_name="John", last_name="Doe", user_id=self.user)
        saved_admin = Administrators.objects.get(id=admin.id)
        self.assertEqual(saved_admin.first_name, "John")
        self.assertEqual(saved_admin.last_name, "Doe")
