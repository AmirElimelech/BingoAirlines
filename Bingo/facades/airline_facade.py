
import logging
from .facade_base import FacadeBase
from ..utils.login_token import LoginToken 
from django.core.exceptions import ValidationError
from ..models import Airline_Companies, Flights , Countries

 

loggin = logging.getLogger(__name__)

        


class AirlineFacade(FacadeBase):

    """
    Facade class for airline-related operations. Inherits from the base facade, FacadeBase.
    It provides methods specific to airline operations and acts as an interface for airline-related requests.
    """

    def __init__(self, request, user, login_token_dict):

        """
        Initialize the AirlineFacade with the request, user, and login token details.

        :param request: The incoming request object.
        :param user: The authenticated user instance.
        :param login_token_dict: Dictionary containing user ID and user role details for generating a login token.
        """

        super().__init__(request, login_token_dict)
        self.user = user
        self.login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
        

    # def validate_airline_privileges(self):
    #     user_role = self.login_token.user_role
    #     if user_role != "airline company":
    #         logging.info("User does not have the necessary privileges to perform this operation.")
    #         raise PermissionError("You do not have the necessary privileges to perform this operation.")

    #     logging.info(f"Trying to fetch airline company for user: {self.user.username}")
        
    #     # Get the associated airline company for the user
    #     airline_company = self.user.airline_companies_set.first()
    #     if airline_company:
    #         iata_code = airline_company.iata_code
    #     else:
    #         logging.error("No associated airline company for user.")
    #         raise ValidationError("No associated airline company for user.")
    #     logging.info(f"Fetched airline company: {airline_company}")
        
    #     # Check if the airline company exists
    #     if not airline_company:
    #         logging.info("Airline company not found")
    #         raise ValidationError("Airline company not found.")
    #     logging.info("Airline company found")

    #     return airline_company


    def validate_airline_privileges(self):
        """
        Validate that the user has the necessary privileges to perform operations related to airline companies.
        Returns the associated airline company for the user if valid.
        """
        try:
            user_role = self.login_token.user_role
            if user_role != "airline company":
                logging.info("User does not have the necessary privileges to perform this operation.")
                raise PermissionError("You do not have the necessary privileges to perform this operation.")

            logging.info(f"Trying to fetch airline company for user: {self.user.username}")
            
            # Get the associated airline company for the user
            airline_company = self.user.airline_companies_set.first()
            
            # Check if the airline company exists
            if not airline_company:
                logging.info("Airline company not found")
                raise ValidationError("Airline company not found.")
            logging.info("Airline company found")

            return airline_company

        except ValidationError as ve:
            logging.error(f"Validation error: {ve}")
            raise ve

        except PermissionError as pe:
            logging.error(f"Permission error: {pe}")
            raise pe

        except Exception as e:
            logging.error(f"Unexpected error during airline privileges validation: {e}")
            raise


    
    # def validate_flight_data(self, flight):
    #     if flight.get("remaining_tickets") <= 0:
    #         logging.info("Number of remaining tickets should be greater than 0.")
    #         raise ValidationError("Number of remaining tickets should be greater than 0.")
    #     if flight.get("landing_time") <= flight.get("departure_time"):
    #         logging.info("Landing time can't be before or equal to departure time.")
    #         raise ValidationError("Landing time can't be before or equal to departure time.")

    def validate_flight_data(self, flight):
        """
        Validate the provided flight data for correctness.

        :param flight: Dictionary containing flight details.
        :raises ValidationError: If the flight data is not valid.
        """

        try:
            # Ensure the number of remaining tickets is positive
            if flight.get("remaining_tickets") <= 0:
                logging.info("Number of remaining tickets should be greater than 0.")
                raise ValidationError("Number of remaining tickets should be greater than 0.")

            # Ensure the landing time is after the departure time
            if flight.get("landing_time") <= flight.get("departure_time"):
                logging.info("Landing time can't be before or equal to departure time.")
                raise ValidationError("Landing time can't be before or equal to departure time.")

        except ValidationError as ve:
            logging.error(f"Validation error in flight data: {ve}")
            raise ve
        except Exception as e:
            logging.error(f"Unexpected error during flight data validation: {e}")
            raise



    # def get_my_flights(self):
    #     self.validate_airline_privileges()
    #     logging.info("getting flights")
        
    #     # Get the associated airline company for the user
    #     airline_company = self.user.airline_companies_set.first()
    #     logging.info(f"Associated airline company for user {self.user.username}: {airline_company}")
        
    #     if not airline_company:
    #         raise Exception("User is not associated with an airline company.")
        
    #     return self.DAL.get_flights_by_airline_id(airline_company.iata_code)


    def get_my_flights(self):
        """
        Retrieve all the flights associated with the airline company linked to the current user.

        :return: Flights associated with the airline company.
        :raises Exception: If the user is not associated with an airline company.
        """

        try:
            # Ensure the user has the correct privileges to access this method
            self.validate_airline_privileges()
            logging.info("Getting flights for the airline company associated with the user.")
            
            # Get the associated airline company for the user
            airline_company = self.user.airline_companies_set.first()
            logging.info(f"Associated airline company for user {self.user.username}: {airline_company}")
            
            # Check if the user is associated with an airline company
            if not airline_company:
                logging.error("User is not associated with an airline company.")
                raise Exception("User is not associated with an airline company.")
            
            # Return flights for the associated airline company
            return self.DAL.get_flights_by_airline_id(airline_company.iata_code)
        
        except ValidationError as ve:
            logging.error(f"Validation error while retrieving flights: {ve}")
            raise ve
        except Exception as e:
            logging.error(f"Unexpected error during flight retrieval: {e}")
            raise



    # def add_flight(self, flight):
    #     self.validate_airline_privileges()
    #     self.validate_flight_data(flight)
        
    #     # Get the associated airline company for the user
    #     airline_company = self.user.airline_companies_set.first()
    #     if not airline_company:
    #         raise PermissionError("User is not associated with any airline company.")
        
    #     if flight.get("airline_company_id") != airline_company.iata_code:
    #         raise PermissionError("Airline companies can only add flights for their own company.")
        
    #     # Fetch the Airline_Companies instance for the given iata_code
    #     airline_company_instance = self.DAL.get_by_id(Airline_Companies, flight.get("airline_company_id"))
    #     if not airline_company_instance:
    #         raise ValidationError(f"No airline company found with iata_code {flight.get('airline_company_id')}")
        
    #     # Fetch the Countries instance for the given origin_country_id and destination_country_id
    #     origin_country_instance = self.DAL.get_by_id(Countries, flight.get("origin_country_id"))
    #     destination_country_instance = self.DAL.get_by_id(Countries, flight.get("destination_country_id"))
    #     if not origin_country_instance or not destination_country_instance:
    #         raise ValidationError("Invalid origin or destination country ID")

    #     # Replace the airline_company_id, origin_country_id, and destination_country_id in the flight data with the actual instances
    #     flight["airline_company_id"] = airline_company_instance
    #     flight["origin_country_id"] = origin_country_instance
    #     flight["destination_country_id"] = destination_country_instance

    #     return self.DAL.add(Flights, **flight)

    def add_flight(self, flight):

        """
        Add a new flight for the airline company associated with the current user after validating the flight data and user privileges.

        :param flight: Dictionary containing flight data.
        :return: Newly created flight instance.
        :raises PermissionError: If the user is not associated with an airline company or tries to add a flight for a different company.
        :raises ValidationError: If the data provided for the flight is invalid.
        """

        try:
            # Ensure the user has the correct privileges to access this method
            self.validate_airline_privileges()
            # Validate the flight data provided
            self.validate_flight_data(flight)
            
            # Get the associated airline company for the user
            airline_company = self.user.airline_companies_set.first()
            if not airline_company:
                raise PermissionError("User is not associated with any airline company.")
            
            # Ensure that the flight being added belongs to the airline company associated with the user
            if flight.get("airline_company_id") != airline_company.iata_code:
                raise PermissionError("Airline companies can only add flights for their own company.")
            
            # Fetch the Airline_Companies instance for the given iata_code
            airline_company_instance = self.DAL.get_by_id(Airline_Companies, flight.get("airline_company_id"))
            if not airline_company_instance:
                raise ValidationError(f"No airline company found with iata_code {flight.get('airline_company_id')}")
            
            # Fetch the Countries instance for the given origin_country_id and destination_country_id
            origin_country_instance = self.DAL.get_by_id(Countries, flight.get("origin_country_id"))
            destination_country_instance = self.DAL.get_by_id(Countries, flight.get("destination_country_id"))
            if not origin_country_instance or not destination_country_instance:
                raise ValidationError("Invalid origin or destination country ID")

            # Replace the airline_company_id, origin_country_id, and destination_country_id in the flight data with the actual instances
            flight["airline_company_id"] = airline_company_instance
            flight["origin_country_id"] = origin_country_instance
            flight["destination_country_id"] = destination_country_instance

            # Add the flight using the DAL
            return self.DAL.add(Flights, **flight)

        except PermissionError as pe:
            logging.error(f"Permission error while adding flight: {pe}")
            raise pe
        except ValidationError as ve:
            logging.error(f"Validation error while adding flight: {ve}")
            raise ve
        except Exception as e:
            logging.error(f"Unexpected error during flight addition: {e}")
            raise




    # def update_flight(self, flight):
    #     flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
    #     # Check if the flight exists
    #     if not flight_instance:
    #         raise ValidationError("Flight not found.")

    #     self.validate_airline_privileges()
    #     self.validate_flight_data(flight)
    #     airline_company = self.user.airline_companies_set.first()
    #     if not airline_company:
    #         raise PermissionError("Airline companies can only edit their own flights.")

    #     if "airline_company_id" in flight:
    #         airline_company_instance = self.DAL.get_by_id(Airline_Companies, flight.get("airline_company_id"))
    #         if not airline_company_instance:
    #             raise ValidationError(f"No airline company found with iata_code {flight.get('airline_company_id')}")
    #         flight["airline_company_id"] = airline_company_instance

    #     if "origin_country_id" in flight:
    #         origin_country_instance = self.DAL.get_by_id(Countries, flight.get("origin_country_id"))
    #         if not origin_country_instance:
    #             raise ValidationError("Invalid origin country ID")
    #         flight["origin_country_id"] = origin_country_instance

    #     if "destination_country_id" in flight:
    #         destination_country_instance = self.DAL.get_by_id(Countries, flight.get("destination_country_id"))
    #         if not destination_country_instance:
    #             raise ValidationError("Invalid destination country ID")
    #         flight["destination_country_id"] = destination_country_instance

    #     return self.DAL.update(flight_instance, **flight)


    def update_flight(self, flight):
        """
        Update an existing flight's details after validating the flight data and user privileges.

        :param flight: Dictionary containing updated flight data.
        :return: Updated flight instance.
        :raises PermissionError: If the user tries to update a flight not associated with their airline company.
        :raises ValidationError: If the data provided for the flight is invalid or if the flight is not found.
        """

        try:
            # Retrieve the flight instance using DAL
            flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
            
            # Check if the flight exists
            if not flight_instance:
                raise ValidationError("Flight not found.")

            # Ensure the user has the correct privileges to access this method
            self.validate_airline_privileges()
            # Validate the flight data provided
            self.validate_flight_data(flight)

            # Get the associated airline company for the user
            airline_company = self.user.airline_companies_set.first()
            if not airline_company:
                raise PermissionError("Airline companies can only edit their own flights.")

            # If airline_company_id is provided, validate and fetch its instance
            if "airline_company_id" in flight:
                airline_company_instance = self.DAL.get_by_id(Airline_Companies, flight.get("airline_company_id"))
                if not airline_company_instance:
                    raise ValidationError(f"No airline company found with iata_code {flight.get('airline_company_id')}")
                flight["airline_company_id"] = airline_company_instance

            # If origin_country_id is provided, validate and fetch its instance
            if "origin_country_id" in flight:
                origin_country_instance = self.DAL.get_by_id(Countries, flight.get("origin_country_id"))
                if not origin_country_instance:
                    raise ValidationError("Invalid origin country ID")
                flight["origin_country_id"] = origin_country_instance

            # If destination_country_id is provided, validate and fetch its instance
            if "destination_country_id" in flight:
                destination_country_instance = self.DAL.get_by_id(Countries, flight.get("destination_country_id"))
                if not destination_country_instance:
                    raise ValidationError("Invalid destination country ID")
                flight["destination_country_id"] = destination_country_instance

            # Update the flight using the DAL
            return self.DAL.update(flight_instance, **flight)

        except PermissionError as pe:
            logging.error(f"Permission error while updating flight: {pe}")
            raise pe
        except ValidationError as ve:
            logging.error(f"Validation error while updating flight: {ve}")
            raise ve
        except Exception as e:
            logging.error(f"Unexpected error during flight update: {e}")
            raise


    # def remove_flight(self, flight): #OLLLLDDD i don't think it's needed anymore
    #     flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
    #     if not flight_instance:
    #         raise ValidationError("Flight not found.")

    #     self.validate_airline_privileges()

    #     if flight_instance.airline_company_id.iata_code != self.user.airline_company.iata_code:
    #         raise PermissionError("Airline companies can only delete their own flights.")
        
    #     return self.DAL.remove(flight_instance)




    # def remove_flight(self, flight):
    #     flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
    #     # Check if the flight exists
    #     if not flight_instance:
    #         raise ValidationError("Flight not found.")

    #     self.validate_airline_privileges()
        
    #     # Fetch the airline company associated with the user
    #     airline_company = self.user.airline_companies_set.first()
    #     if not airline_company:
    #         raise PermissionError("User is not associated with any airline company.")
        
    #     if flight_instance.airline_company_id.iata_code != airline_company.iata_code:
    #         raise PermissionError("Airline companies can only delete their own flights.")
        
    #     return self.DAL.remove(flight_instance)



    def remove_flight(self, flight):
        """
        Remove a flight after validating user privileges and ensuring the flight exists.

        :param flight: Dictionary containing details of the flight to be removed.
        :return: Result of the removal operation.
        :raises PermissionError: If the user tries to remove a flight not associated with their airline company.
        :raises ValidationError: If the flight is not found.
        """

        try:
            # Retrieve the flight instance using DAL
            flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
            
            # Check if the flight exists
            if not flight_instance:
                raise ValidationError("Flight not found.")

            # Ensure the user has the correct privileges to access this method
            self.validate_airline_privileges()

            # Fetch the airline company associated with the user
            airline_company = self.user.airline_companies_set.first()
            if not airline_company:
                raise PermissionError("User is not associated with any airline company.")
            
            # Ensure that the flight belongs to the user's airline company
            if flight_instance.airline_company_id.iata_code != airline_company.iata_code:
                raise PermissionError("Airline companies can only delete their own flights.")
            
            # Remove the flight using the DAL
            return self.DAL.remove(flight_instance)

        except PermissionError as pe:
            logging.error(f"Permission error while removing flight: {pe}")
            raise pe
        except ValidationError as ve:
            logging.error(f"Validation error while removing flight: {ve}")
            raise ve
        except Exception as e:
            logging.error(f"Unexpected error during flight removal: {e}")
            raise






