import re , logging
from ..utils.login_token import LoginToken
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from ..models import DAL, Users, Airline_Companies, Flights, Countries , User_Roles , Administrators , Customers




logger = logging.getLogger(__name__)



class FacadeBase:
    def __init__(self, request, login_token: LoginToken=None):   

        """
        Initialize the FacadeBase object with request, a DAL instance, and an optional login token.
        """

        self.DAL = DAL()
        self.request = request
        self.login_token = login_token
        

    def get_all_flights(self):

        """
        Retrieve all flight records from the database.
        """

        logging.info("getting All Flights")
        return self.DAL.get_all(Flights)
        


    def get_flight_by_id(self, id):

        """
        Retrieve a specific flight record from the database based on its ID.
        """
         
        logging.info("getting Flight by id")
        return self.DAL.get_by_id(Flights, id)



    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):

        """
        Retrieve flight records from the database based on origin country, destination country, and date.
        """

        logging.info("getting Flights by parameters")
        return self.DAL.get_flights_by_parameters(origin_country_id, destination_country_id, date)



    def get_all_airlines(self):

        """
        Retrieve all airline company records from the database.
        """

        logging.info("getting All Airlines")
        return self.DAL.get_all(Airline_Companies)



    def get_airline_by_id(self, iata_code):

        """
        Retrieve a specific airline record from the database based on its IATA code.
        """

        logging.info("getting Airline by id")
        return self.DAL.get_by_id(Airline_Companies, iata_code)



    def get_all_countries(self):

        """
        Retrieve all country records from the database.
        """

        logging.info("getting All Countries")
        return self.DAL.get_all(Countries)



    def get_country_by_id(self, country_code):

        """
        Retrieve a specific country record from the database based on its country code.
        """

        logging.info("getting Country by id")
        # return self.DAL.get_by_id(Countries, country_code)
        return self.DAL.get_by_id(Countries, country_code, field_name='country_code')




    @csrf_exempt
    def create_new_user(self, user):

        """
        Validate user input data and create a new user record in the database.
        Ensures the ID, username, email, password, user role, and phone number are valid before creating the user.
        """

        try:
            # ID Validity
            if not re.match(r"^\d{9}$", user.get("id")):
                logging.error("ID should be exactly 9 digits.")
                raise ValidationError("ID should be exactly 9 digits.")
                    
            # Username Validity
            if not (3 <= len(user.get("username")) <= 20) or not re.match(r"^\w+$", user.get("username")):
                logging.error("Username should be between 3 and 20 characters and contain only alphanumeric characters and underscores.")
                raise ValidationError("Username should be between 3 and 20 characters and contain only alphanumeric characters and underscores.")

            # Email Validity
            if Users.objects.filter(email=user.get("email")).exists():
                logging.error("Email already exists")
                raise ValidationError("Email already exists")
            

            # Password Strength
            password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"
            if len(user.get("password")) < 6 or not re.match(password_pattern, user.get("password")):
                logging.error("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")
                raise ValidationError("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")

            # User Role Validity
            if not User_Roles.objects.filter(role_name=user.get("user_role")).exists():
                logging.error("Provided user role does not exist.")
                raise ValidationError("Provided user role does not exist.")
                
            # Phone number validity assuming phone number is unique and does not exist in the database
            if Customers.objects.filter(phone_no=user.get("phone_no")).exists():
                logging.error("Phone number already exists.")
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
            
            if not created_user:
                logging.error(f"Failed to create Users instance with data: {user_data}")
                raise Exception("Failed to create the user.")

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
