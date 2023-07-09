from .facade_base import FacadeBase
from Bingo.models import Flights, Airline_Companies

class AirlineFacade(FacadeBase):

    def get_my_flights(self, airline_id):
        return self._dal.get_flights_by_airline_id(airline_id)

    def update_airline(self, airline):
        return self._dal.update(Airline_Companies, **airline)

    def add_flight(self, flight):
        return self._dal.add(Flights, **flight)

    def update_flight(self, flight):
        return self._dal.update(Flights, **flight)

    def remove_flight(self, flight):
        return self._dal.remove(flight)
