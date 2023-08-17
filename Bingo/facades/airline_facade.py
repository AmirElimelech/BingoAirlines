
from .facade_base import FacadeBase
from ..models import Airline_Companies, Flights
from django.core.exceptions import ValidationError
from ..utils.login_token import LoginToken  # Import LoginToken class
import logging


loggin = logging.getLogger(__name__)


class AirlineFacade(FacadeBase):
    def __init__(self, request, user, login_token: LoginToken=None):  # Add the login_token parameter with type annotation
        super().__init__(request, login_token)  # Pass the login_token object to the parent constructor
        self.user = user


    def validate_airline_company(self):
        self.validate_login_token(self.login_token) 
        # Fetch the airline company
        airline_company = self.DAL.get_by_id(Airline_Companies, self.user.airline_company.iata_code)
        
        # Check if the airline company exists
        if not airline_company:
            loggin.info("Airline company not found")
            raise ValidationError("Airline company not found.")
        loggin.info("Airline company found")

        return airline_company

    def validate_flight_data(self, flight):
        if flight.get("remaining_tickets") <= 0:
            loggin.info("Number of remaining tickets should be greater than 0.")
            raise ValidationError("Number of remaining tickets should be greater than 0.")
        if flight.get("landing_time") <= flight.get("departure_time"):
            loggin.info("Landing time can't be before or equal to departure time.")
            raise ValidationError("Landing time can't be before or equal to departure time.")

    def get_my_flights(self):
        self.validate_airline_company()
        loggin.info("getting flights")
        return self.DAL.get_flights_by_airline_id(self.user.airline_company.iata_code)

    def add_flight(self, flight):
        self.validate_airline_company()
        self.validate_flight_data(flight)
        
        if flight.get("airline_company_id") != self.user.airline_company.iata_code:
            raise PermissionError("Airline companies can only add flights for their own company.")
        
        return self.DAL.add(Flights, **flight)

    def update_flight(self, flight):
        flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
        # Check if the flight exists
        if not flight_instance:
            raise ValidationError("Flight not found.")

        self.validate_airline_company()
        self.validate_flight_data(flight)
        
        if flight_instance.airline_company_id.iata_code != self.user.airline_company.iata_code:
            raise PermissionError("Airline companies can only edit their own flights.")
        
        for attr, value in flight.items():
            setattr(flight_instance, attr, value)
        flight_instance.save()

        return flight_instance

    def remove_flight(self, flight):
        flight_instance = self.DAL.get_by_id(Flights, flight.get("id"))
        
        if not flight_instance:
            raise ValidationError("Flight not found.")

        self.validate_airline_company()

        if flight_instance.airline_company_id.iata_code != self.user.airline_company.iata_code:
            raise PermissionError("Airline companies can only delete their own flights.")
        
        return self.DAL.remove(flight_instance)



