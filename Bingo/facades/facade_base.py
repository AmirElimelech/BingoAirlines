from ..models import DAL, Users, Airline_Companies, Flights, Countries , User_Roles , Administrators , Customers
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re
import logging
from django.views.decorators.csrf import csrf_exempt


class CustomUserCreationError(Exception):
    def __init__(self, errors):
        self.errors = errors

class FacadeBase:
    def __init__(self, request=None):
        self.DAL = DAL()
        self.request = request


    def validate_session(self):
        if 'user_id' not in self.request.session:
            raise PermissionError("Session expired. Please login again.")
    
    def get_all_flights(self):
        return self.DAL.get_all(Flights)

    def get_flight_by_id(self, id):
        return self.DAL.get_by_id(Flights, id)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        return self.DAL.get_flights_by_parameters(origin_country_id, destination_country_id, date)

    def get_all_airlines(self):
        return self.DAL.get_all(Airline_Companies)

    def get_airline_by_id(self, id):
        return self.DAL.get_by_id(Airline_Companies, id)

    def get_all_countries(self):
        return self.DAL.get_all(Countries)

    def get_country_by_id(self, id):
        return self.DAL.get_by_id(Countries, id)

    @csrf_exempt
    def create_new_user(self, user):
        try:
            # ID Validity
            if not re.match(r"^\d{9}$", user.get("id")):
                raise ValidationError("ID should be exactly 9 digits.")
                    
            # Username Validity
            if not (3 <= len(user.get("username")) <= 20) or not re.match(r"^\w+$", user.get("username")):
                raise ValidationError("Username should be between 3 and 20 characters and contain only alphanumeric characters and underscores.")

            # Email Validity
            if Users.objects.filter(email=user.get("email")).exists():
                raise ValidationError("Email already exists")

            # Password Strength
            password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
            if len(user.get("password")) < 6 or not re.match(password_pattern, user.get("password")):
                raise ValidationError("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")

            # User Role Validity
            if not User_Roles.objects.filter(role_name=user.get("user_role")).exists():
                raise ValidationError("Provided user role does not exist.")
                
            # Phone number validity assuming phone number is unique and does not exist in the database
            if Customers.objects.filter(phone_no=user.get("phone_no")).exists():
                raise ValidationError("Phone number already exists.")
            
            password = make_password(user.get("password"))  # hash the password before saving
            user_data = {
                'id': user.get("id"),
                'username': user.get("username"),
                'email': user.get("email"),
                'password': password,
                'user_role': user.get("user_role"),
                'image': user.get("image")
            }
            logging.info(f"User data: {user_data}")
            created_user = self.DAL.add(Users, **user_data)
            
            # Check if created_user is None or not the expected type
            if not created_user:
                logging.error("Failed to create the user using DAL.add method.")
                return {"status": "error", "message": "Failed to create the user."}

            return created_user

        except ValidationError as ve:
            logging.error(f"Validation Error: {ve}")
            return {"status": "error", "message": str(ve)}
        
        except KeyError as ke:
            logging.error(f"KeyError during user creation: {ke}")
            return {"status": "error", "message": f"Failed accessing key: {ke}"}

        except Exception as e:
            logging.error(f"Unexpected Error during user creation: {e}")
            return {"status": "error", "message": "An unexpected error occurred during user creation."}
