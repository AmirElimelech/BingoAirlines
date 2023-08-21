from .facade_base import FacadeBase
from ..models import Airline_Companies, Flights , Countries
from django.core.exceptions import ValidationError
from ..utils.login_token import LoginToken  
import logging


loggin = logging.getLogger(__name__)

        
class AirlineFacade(FacadeBase):
    def __init__(self, request, user, login_token_dict):
        super().__init__(request, login_token_dict)
        self.user = user
        self.login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
        

    def validate_airline_privileges(self):
        user_role = self.login_token.user_role
        if user_role != "airline company":
            logging.info("User does not have the necessary privileges to perform this operation.")
            raise PermissionError("You do not have the necessary privileges to perform this operation.")

        logging.info(f"Trying to fetch airline company for user: {self.user.username}")
        
        # Get the associated airline company for the user
        airline_company = self.user.airline_companies_set.first()
        if airline_company:
            iata_code = airline_company.iata_code
        else:
            logging.error("No associated airline company for user.")
            raise ValidationError("No associated airline company for user.")
        logging.info(f"Fetched airline company: {airline_company}")
        
        # Check if the airline company exists
        if not airline_company:
            logging.info("Airline company not found")
            raise ValidationError("Airline company not found.")
        logging.info("Airline company found")

        return airline_company

    
    def validate_flight_data(self, flight):
        if flight.get("remaining_tickets") <= 0:
            logging.info("Number of remaining tickets should be greater than 0.")
            raise ValidationError("Number of remaining tickets should be greater than 0.")
        if flight.get("landing_time") <= flight.get("departure_time"):
            logging.info("Landing time can't be before or equal to departure time.")
            raise ValidationError("Landing time can't be before or equal to departure time.")


    def get_my_flights(self):
        self.validate_airline_privileges()
        logging.info("getting flights")
        
        # Get the associated airline company for the user
        airline_company = self.user.airline_companies_set.first()
        logging.info(f"Associated airline company for user {self.user.username}: {airline_company}")
        
        if not airline_company:
            raise Exception("User is not associated with an airline company.")
        
        return self.DAL.get_flights_by_airline_id(airline_company.iata_code)


    def add_flight(self, flight):
        self.validate_airline_privileges()
        self.validate_flight_data(flight)
        
        # Get the associated airline company for the user
        airline_company = self.user.airline_companies_set.first()
        if not airline_company:
            raise PermissionError("User is not associated with any airline company.")
        
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

        return self.DAL.add(Flights, **flight)



    def update_flight(self, flight):
        flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
        # Check if the flight exists
        if not flight_instance:
            raise ValidationError("Flight not found.")

        self.validate_airline_privileges()
        self.validate_flight_data(flight)
        airline_company = self.user.airline_companies_set.first()
        if not airline_company:
            raise PermissionError("Airline companies can only edit their own flights.")

        if "airline_company_id" in flight:
            airline_company_instance = self.DAL.get_by_id(Airline_Companies, flight.get("airline_company_id"))
            if not airline_company_instance:
                raise ValidationError(f"No airline company found with iata_code {flight.get('airline_company_id')}")
            flight["airline_company_id"] = airline_company_instance

        if "origin_country_id" in flight:
            origin_country_instance = self.DAL.get_by_id(Countries, flight.get("origin_country_id"))
            if not origin_country_instance:
                raise ValidationError("Invalid origin country ID")
            flight["origin_country_id"] = origin_country_instance

        if "destination_country_id" in flight:
            destination_country_instance = self.DAL.get_by_id(Countries, flight.get("destination_country_id"))
            if not destination_country_instance:
                raise ValidationError("Invalid destination country ID")
            flight["destination_country_id"] = destination_country_instance

        return self.DAL.update(flight_instance, **flight)

    # def remove_flight(self, flight):
    #     flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
    #     if not flight_instance:
    #         raise ValidationError("Flight not found.")

    #     self.validate_airline_privileges()

    #     if flight_instance.airline_company_id.iata_code != self.user.airline_company.iata_code:
    #         raise PermissionError("Airline companies can only delete their own flights.")
        
    #     return self.DAL.remove(flight_instance)

    def remove_flight(self, flight):
        flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
        # Check if the flight exists
        if not flight_instance:
            raise ValidationError("Flight not found.")

        self.validate_airline_privileges()
        
        # Fetch the airline company associated with the user
        airline_company = self.user.airline_companies_set.first()
        if not airline_company:
            raise PermissionError("User is not associated with any airline company.")
        
        if flight_instance.airline_company_id.iata_code != airline_company.iata_code:
            raise PermissionError("Airline companies can only delete their own flights.")
        
        return self.DAL.remove(flight_instance)





