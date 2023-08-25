from django.test import TestCase
from Bingo.models import User_Roles
from django.core.exceptions import ValidationError

class UserRolesModelTest(TestCase):

        @classmethod
        def setUpTestData(cls):
            # Set up non-modified objects used by all test methods
            User_Roles.objects.create(role_name="Admin")


        def test_role_name_label(self):
            role = User_Roles.objects.get(id=1)
            field_label = role._meta.get_field('role_name').verbose_name
            self.assertEqual(field_label, 'role name')

        def test_role_name_max_length(self):
            role = User_Roles.objects.get(id=1)
            max_length = role._meta.get_field('role_name').max_length
            self.assertEqual(max_length, 255)

        def test_role_name_unique(self):
            role = User_Roles.objects.get(id=1)
            unique = role._meta.get_field('role_name').unique
            self.assertEqual(unique, True)

        
        def test_object_name_is_role_name(self):
            role = User_Roles.objects.get(id=1)
            expected_object_name = role.role_name
            self.assertEqual(str(role), expected_object_name)

        def test_valid_role_name(self):
            role = User_Roles(role_name="Customer")
            role.save()
            self.assertEqual(role.role_name, "Customer")

        def test_invalid_role_name(self):
            role = User_Roles(role_name="InvalidRole")
            with self.assertRaises(ValidationError):
                role.save()

        def test_clean_method_with_valid_role(self):
            role = User_Roles(role_name="AirlineCompany")
            role.clean()  # Should not raise any exception

        def test_clean_method_with_invalid_role(self):
            role = User_Roles(role_name="InvalidRole")
            with self.assertRaises(ValidationError):
                role.clean()
