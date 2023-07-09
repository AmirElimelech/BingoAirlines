from abc import ABC, abstractmethod
from Bingo.models import DAL
from BingoAirlines.Bingo.models import Flights , Countries , Airline_Companies , Users , Customers
from django.contrib.auth.hashers import make_password




class FacadeBase(ABC):

    def __init__(self):
        self.dal = DAL()

    def get_all_flights(self):
        return self.dal.get_all(Flights)

    def get_flight_by_id(self, id):
        return self.dal.get_by_id(Flights, id)

    def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):
        return self.dal.get_flights_by_parameters(origin_country_id, destination_country_id, date)

    def get_all_airlines(self):
        return self.dal.get_all(Airline_Companies)

    def get_airline_by_id(self, id):
        return self.dal.get_by_id(Airline_Companies, id)

    def get_all_countries(self):
        return self.dal.get_all(Countries)

    def get_country_by_id(self, id):
        return self.dal.get_by_id(Countries, id)

    def create_new_user(self, user):
        # assuming 'user' is a dictionary containing the details of the user
        user['password'] = make_password(user['password'])
        return self.dal.add(Users, **user)