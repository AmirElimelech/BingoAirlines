# from abc import ABC, abstractmethod
# from Bingo.models import DAL
# from django.contrib.auth.hashers import make_password
# from models import Users, Airline_Companies, Flights, Countries




# class FacadeBase(ABC):

#     def __init__(self):
#         self.dal = DAL()

#     def get_all_flights(self):
#         return self.dal.get_all(Flights)

#     def get_flight_by_id(self, id):
#         return self.dal.get_by_id(Flights, id)

#     def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
#         return self.dal.get_flights_by_parameters(origin_country_id, destination_country_id, date)

#     def get_all_airlines(self):
#         return self.dal.get_all(Airline_Companies)
    
#     def get_airline_by_parameters(self, country_id=None):
#         airlines = self.dal.get_all(Airline_Companies)
        
#         if country_id is not None:
#             airlines = airlines.filter(country_id=country_id)
        
#         return airlines
    
#     def get_airline_by_id(self, id):
#         return self.dal.get_by_id(Airline_Companies, id)

#     def get_all_countries(self):
#         return self.dal.get_all(Countries)

#     def get_country_by_id(self, id):
#         return self.dal.get_by_id(Countries, id)

#     def create_new_user(self, user):
#         # assuming 'user' is a dictionary containing the details of the user
#         user['password'] = make_password(user['password'])
#         return self.dal.add(Users, **user)
    



# ------------------------------------------------------------------------------------------------------------------------------




from models import DAL, Users, Airline_Companies, Flights, Countries
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)

class FacadeBase:
    def __init__(self):
        self.DAL = DAL()
    
    def get_all_flights(self):
        try:
            return self.DAL.get_all(Flights)
        except Exception as e:
            logger.error(f"Error getting all flights: {e}")
            return None

    def get_flight_by_id(self, id):
        try:
            return self.DAL.get_by_id(Flights, id)
        except Exception as e:
            logger.error(f"Error getting flight by id: {e}")
            return None

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        try:
            return self.DAL.get_flights_by_parameters(origin_country_id, destination_country_id, date)
        except Exception as e:
            logger.error(f"Error getting flights by parameters: {e}")
            return None

    def get_all_airlines(self):
        try:
            return self.DAL.get_all(Airline_Companies)
        except Exception as e:
            logger.error(f"Error getting all airlines: {e}")
            return None

    def get_airline_by_id(self, id):
        try:
            return self.DAL.get_by_id(Airline_Companies, id)
        except Exception as e:
            logger.error(f"Error getting airline by id: {e}")
            return None
    
    def get_airline_by_parameters(self, country_id=None):
        try:
            airlines = self.DAL.get_all(Airline_Companies)
            if country_id is not None:
                airlines = airlines.filter(country_id=country_id)
            return airlines
        except Exception as e:
            logger.error(f"Error getting airlines by parameters: {e}")
            return None

    def get_all_countries(self):
        try:
            return self.DAL.get_all(Countries)
        except Exception as e:
            logger.error(f"Error getting all countries: {e}")
            return None

    def get_country_by_id(self, id):
        try:
            return self.DAL.get_by_id(Countries, id)
        except Exception as e:
            logger.error(f"Error getting country by id: {e}")
            return None

    def create_new_user(self, user):
        try:
            # Hash the password before storing
            user['password'] = generate_password_hash(user['password'])
            return self.DAL.add(Users, **user)
        except Exception as e:
            logger.error(f"Error creating new user: {e}")
            return None
