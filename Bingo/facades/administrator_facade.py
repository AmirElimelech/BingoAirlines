from .facade_base import FacadeBase
from ..models import Customers, Airline_Companies, Administrators , Users , Countries
from django.core.exceptions import ValidationError
from ..utils.login_token import LoginToken
import logging

logger = logging.getLogger(__name__)



# class AdministratorFacade(FacadeBase):
#     def __init__(self, request, user, login_token: LoginToken):  # Add the login_token parameter with type annotation
#         super().__init__(request, login_token) 
#         self.request = request
#         self.user = user
#         self.login_token = login_token  # Store   # Store the login_token object

#     def validate_admin_privileges(self):
#         # Validate the user role from the LoginToken object
#         user_role = self.login_token.user_role  # Replace session access with login_token access
#         if user_role != "administrator":
#             logging.info("User does not have the necessary privileges to perform this operation.")
#             raise PermissionError("You do not have the necessary privileges to perform this operation.")

class AdministratorFacade(FacadeBase):
    def __init__(self, request, user, login_token: LoginToken=None):
        super().__init__(request, login_token) 
        self.user = user

    

    def validate_admin_privileges(self):
        if not self.login_token:
            logging.error("Login token is missing.")
            raise PermissionError("Login token is missing.")
    
        user_role = self.login_token.user_role
        if user_role != "administrator":
            logging.info("User does not have the necessary privileges to perform this operation.")
            raise PermissionError("You do not have the necessary privileges to perform this operation.")





    def get_all_customers(self):
        self.validate_admin_privileges()
        logging.info("getting All Customers")
        return self.DAL.get_all(Customers)
    






    def add_airline(self, airline):

        self.validate_admin_privileges()
        logging.info("Admin previleges validated")

        iata_code = airline['iata_code'].upper()
        if iata_code != airline['iata_code']:
            logging.error("IATA code must be in uppercase.")
            raise ValidationError("IATA code must be in uppercase.")
        
        if Airline_Companies.objects.filter(name=airline['name']).exists():
            logging.error("Airline with this name already exists.")
            raise ValidationError("Airline with this name already exists.")
        
        if Airline_Companies.objects.filter(iata_code=airline['iata_code']).exists():
            logging.error("Airline with this IATA code already exists.")
            raise ValidationError("Airline with this IATA code already exists.")
        

        
        # Retrieve the Countries instance using the provided ID
        country_instance = Countries.objects.get(pk=airline['country_id'])

        # Replace the 'country_id' in the airline dictionary with the actual instance
        airline['country_id'] = country_instance

        # Retrieve the Users instance using the provided ID
        user_instance = Users.objects.get(id=airline['user_id'])

        # Replace the 'user_id' in the airline dictionary with the actual instance
        airline['user_id'] = user_instance
        
        logging.info("Adding Airline successfully")
        return self.DAL.add(Airline_Companies, **airline)
    




    def add_customer(self, customer):
        self.validate_admin_privileges()
        logging.info("Admin previleges validated")

        # Validate phone number
        if Customers.objects.filter(phone_no=customer['phone_no']).exists():
            logging.error("Customer with this phone number already exists.")
            raise ValidationError("Customer with this phone number already exists.")
        
        
        

        # Retrieve the Users instance using the provided ID
        user_instance = Users.objects.get(id=customer['user_id'])

        # Replace the 'user_id' in the customer dictionary with the actual instance
        customer['user_id'] = user_instance
            

        logging.info("Adding Customer successfully")
        return self.DAL.add(Customers, **customer)
    




    def add_administrator(self, administrator):
        self.validate_admin_privileges()
        logging.info("Admin previleges validated")
        
        def is_valid_name(name):
            return all(c.isalpha() or c.isspace() or c == '-' for c in name)

        if not is_valid_name(administrator["first_name"]) or not is_valid_name(administrator["last_name"]):
            logging.error("Names should only contain letters, spaces, and hyphens.")
            raise ValidationError("Names should only contain letters, spaces, and hyphens.")
        
        if Administrators.objects.filter(user_id=administrator['user_id']).exists():
            logging.error("This user already has an administrator account.")
            raise ValidationError("This user already has an administrator account.")
        

        

        # Retrieve the Users instance using the provided ID
        user_instance = Users.objects.get(id=administrator['user_id'])

        # Replace the 'user_id' in the administrator dictionary with the actual instance
        administrator['user_id'] = user_instance



        logging.info("Adding Administrator successfully")
        return self.DAL.add(Administrators, **administrator)








    def remove_airline(self, airline):
        self.validate_admin_privileges()
        logging.info("Admin previleges validated")


        airline_instance = self.DAL.get_by_id(Airline_Companies, airline.get("iata_code"))
        if not airline_instance:
            logging.error("Airline not found.")
            raise ValidationError("Airline not found.")
        
        logging.info("Removing Airline successfully")
        return self.DAL.remove(airline_instance)

    def remove_customer(self, customer):
        self.validate_admin_privileges()
        logging.info("Admin previleges validated")


        customer_instance = self.DAL.get_by_id(Customers, customer.get("id"))
        if not customer_instance:
            logging.error("Customer not found.")
            raise ValidationError("Customer not found.")
        
        logging.info("Removing Customer successfully")
        return self.DAL.remove(customer_instance)

    def remove_administrator(self, administrator):
        self.validate_admin_privileges()
        logging.info("Admin previleges validated")


        admin_instance = self.DAL.get_by_id(Administrators, administrator.get("id"))
        if not admin_instance:
            logging.error("Administrator not found.")
            raise ValidationError("Administrator not found.")
        
        logging.info("Removing Administrator successfully")
        return self.DAL.remove(admin_instance)


