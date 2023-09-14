import logging
from .facade_base import FacadeBase
from ..utils.login_token import LoginToken
from django.core.exceptions import ValidationError
from ..models import Customers, Airline_Companies, Administrators , Users , Countries , DAL


logger = logging.getLogger(__name__)



class AdministratorFacade(FacadeBase):

    """
    Facade for Administrator-related operations. This class contains methods specific to 
    administrative tasks and ensures that only users with administrative privileges can 
    perform certain operations.
    """

    def __init__(self, request, user, login_token: LoginToken=None):

        """
        Initialize the AdministratorFacade with the given request, user, and an optional login token.

        :param request: The HTTP request object.
        :param user: The user object associated with the current session/request.
        :param login_token: (Optional) A token that represents the login session of the user.
        """
         
        super().__init__(request, login_token) 
        self.user = user

    

    def validate_admin_privileges(self):
        """
        Ensure the user has administrative privileges before allowing certain operations.

        :raises PermissionError: If the user doesn't have the required privileges or if the login token is missing.
        """
        
        try:
            # Check if the login token is present
            if not self.login_token:
                logging.error("Login token is missing.")
                raise PermissionError("Login token is missing.")
        
            # Retrieve the user role from the login token
            user_role = self.login_token.get('user_role', None)


            # Ensure that the user role is 'administrator'
            if user_role != "Administrator":
                logging.error("User does not have the necessary privileges to perform this operation.")
                raise PermissionError("You do not have the necessary privileges to perform this operation.")
        
        except PermissionError as pe:
            logging.error(f"Permission error: {pe}")
            raise pe
        except Exception as e:
            logging.error(f"Unexpected error during privilege validation: {e}")
            raise


    def get_all_customers(self):
        """
        Fetch all customer records from the database. This method ensures that 
        only users with administrative privileges can retrieve all customers.

        :return: A queryset containing all customers.
        """
        try:
            # Validate if the user has administrative privileges
            self.validate_admin_privileges()
            
            logging.info("Fetching all customers.")
            
            # Use the DAL to get all customer records
            return self.DAL.get_all(Customers)
        except PermissionError as pe:
            logging.error(f"Permission error while fetching all customers: {pe}")
            raise pe
        except Exception as e:
            logging.error(f"Unexpected error while fetching all customers: {e}")
            raise



    
    def add_airline(self, airline):
        """
        Add a new airline to the database after validating the provided information and ensuring
        that the user has administrative privileges.
        
        :param airline: A dictionary containing the details of the airline to be added.
        :return: The newly created airline instance.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")

            # Convert the IATA code to uppercase and validate
            iata_code = airline['iata_code'].upper()
            if iata_code != airline['iata_code']:
                logging.error("IATA code must be in uppercase.")
                raise ValidationError("IATA code must be in uppercase.")
            
            # Check for existing airlines with the same name
            if Airline_Companies.objects.filter(name=airline['name']).exists():
                logging.error("Airline with this name already exists.")
                raise ValidationError("Airline with this name already exists.")
            
            # Check for existing airlines with the same IATA code
            if Airline_Companies.objects.filter(iata_code=airline['iata_code']).exists():
                logging.error("Airline with this IATA code already exists.")
                raise ValidationError("Airline with this IATA code already exists.")
            
            # Fetch the associated country instance for the provided ID
            country_instance = Countries.objects.get(pk=airline['country_id'])
            airline['country_id'] = country_instance
            
            # Fetch the associated user instance for the provided ID
            user_instance = Users.objects.get(id=airline['user_id'])
            airline['user_id'] = user_instance
            
            # Finally, add the airline to the database
            logging.info("Adding Airline successfully")
            return self.DAL.add(Airline_Companies, **airline)

        # Handle specific validation errors
        except ValidationError as ve:
            logging.error(f"Validation error while adding airline: {ve}")
            raise ve
        
        # Handle all other unexpected errors
        except Exception as e:
            logging.error(f"Unexpected error while adding airline: {e}")
            raise

    

    def add_customer(self, customer):
        """
        Add a new customer to the database after validating the provided information and ensuring
        that the user has administrative privileges.
        
        :param customer: A dictionary containing the details of the customer to be added.
        :return: The newly created customer instance.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")

            # Check for existing customers with the same phone number
            if Customers.objects.filter(phone_no=customer['phone_no']).exists():
                logging.error("Customer with this phone number already exists.")
                raise ValidationError("Customer with this phone number already exists.")
            
            # Fetch the associated user instance for the provided ID
            user_instance = Users.objects.get(id=customer['user_id'])
            customer['user_id'] = user_instance
            
            # Finally, add the customer to the database
            logging.info("Adding Customer successfully")
            return self.DAL.add(Customers, **customer)

        # Handle specific validation errors
        except ValidationError as ve:
            logging.error(f"Validation error while adding customer: {ve}")
            raise ve
        
        # Handle all other unexpected errors
        except Exception as e:
            logging.error(f"Unexpected error while adding customer: {e}")
            raise






    def add_administrator(self, administrator):
        """
        Add a new administrator to the database after validating the provided information and ensuring
        that the user has administrative privileges.
        
        :param administrator: A dictionary containing the details of the administrator to be added.
        :return: The newly created administrator instance.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")
            
            # Helper function to validate names
            def is_valid_name(name):
                return all(c.isalpha() or c.isspace() or c == '-' for c in name)

            # Validate administrator names
            if not is_valid_name(administrator["first_name"]) or not is_valid_name(administrator["last_name"]):
                logging.error("Names should only contain letters, spaces, and hyphens.")
                raise ValidationError("Names should only contain letters, spaces, and hyphens.")
            
            # Check for existing administrators with the same user ID
            if Administrators.objects.filter(user_id=administrator['user_id']).exists():
                logging.error("This user already has an administrator account.")
                raise ValidationError("This user already has an administrator account.")
            
            # Fetch the associated user instance for the provided ID
            user_instance = Users.objects.get(id=administrator['user_id'])
            administrator['user_id'] = user_instance
            
            # Finally, add the administrator to the database
            logging.info("Adding Administrator successfully")
            return self.DAL.add(Administrators, **administrator)

        # Handle specific validation errors
        except ValidationError as ve:
            logging.error(f"Validation error while adding administrator: {ve}")
            raise ve
        
        # Handle all other unexpected errors
        except Exception as e:
            logging.error(f"Unexpected error while adding administrator: {e}")
            raise








    def remove_airline(self, airline):
        """
        Remove an airline from the database after validating the provided information
        and ensuring that the user has administrative privileges.
        
        :param airline: A dictionary containing the details of the airline to be removed.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")

            # Fetch the associated airline instance using the provided IATA code
            airline_instance = self.DAL.get_by_id(Airline_Companies, airline.get("iata_code"))
            if not airline_instance:
                logging.error("Airline not found.")
                raise ValidationError("Airline not found.")
            
            # Remove the airline from the database
            logging.info("Removing Airline successfully")
            return self.DAL.remove(airline_instance)
        
        except ValidationError as ve:
            logging.error(f"Validation error while removing airline: {ve}")
            raise ve
        
        except Exception as e:
            logging.error(f"Unexpected error while removing airline: {e}")
            raise





    def remove_customer(self, customer):
        """
        Remove a customer from the database after validating the provided information
        and ensuring that the user has administrative privileges.
        
        :param customer: A dictionary containing the details of the customer to be removed.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")

            # Fetch the associated customer instance using the provided ID
            customer_instance = self.DAL.get_by_id(Customers, customer.get("id"))
            if not customer_instance:
                logging.error("Customer not found.")
                raise ValidationError("Customer not found.")
            
            # Remove the customer from the database
            logging.info("Removing Customer successfully")
            return self.DAL.remove(customer_instance)
        
        except ValidationError as ve:
            logging.error(f"Validation error while removing customer: {ve}")
            raise ve
        
        except Exception as e:
            logging.error(f"Unexpected error while removing customer: {e}")
            raise

   
   
   

    def remove_administrator(self, administrator):
        """
        Remove an administrator from the database after validating the provided information
        and ensuring that the user has administrative privileges.
        
        :param administrator: A dictionary containing the details of the administrator to be removed.
        """
        try:
            # Validate administrative privileges
            self.validate_admin_privileges()
            logging.info("Admin privileges validated")

            # Fetch the associated administrator instance using the provided ID
            admin_instance = self.DAL.get_by_id(Administrators, administrator.get("id"))
            if not admin_instance:
                logging.error("Administrator not found.")
                raise ValidationError("Administrator not found.")
            
            # Remove the administrator from the database
            logging.info("Removing Administrator successfully")
            return self.DAL.remove(admin_instance)
        
        except ValidationError as ve:
            logging.error(f"Validation error while removing administrator: {ve}")
            raise ve
        
        except Exception as e:
            logging.error(f"Unexpected error while removing administrator: {e}")
            raise







