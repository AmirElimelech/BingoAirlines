# from .facade_base import FacadeBase
# from Bingo.models import Flights, Airline_Companies

# class AirlineFacade(FacadeBase):

#     def get_my_flights(self, airline_id):
#         return self._dal.get_flights_by_airline_id(airline_id)

#     def update_airline(self, airline):
#         return self._dal.update(Airline_Companies, **airline)

#     def add_flight(self, flight):
#         return self._dal.add(Flights, **flight)

#     def update_flight(self, flight):
#         return self._dal.update(Flights, **flight)

#     def remove_flight(self, flight):
#         return self._dal.remove(flight)


# ------------------------------------------------------------------------------------------------------------------------------


from .facade_base import FacadeBase
from models import Airline_Companies, Flights
import logging

logger = logging.getLogger(__name__)

class AirlineFacade(FacadeBase):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def get_my_flights(self):
        try:
            return self.DAL.get_flights_by_airline_id(self.user.airline_company.iata_code)
        except Exception as e:
            logger.error(f"Error getting my flights: {e}")
            return None

    def update_airline(self, airline):
        try:
            return self.DAL.update(self.user.airline_company, **airline)
        except Exception as e:
            logger.error(f"Error updating airline: {e}")
            return None

    def add_flight(self, flight):
        try:
            return self.DAL.add(Flights, **flight)
        except Exception as e:
            logger.error(f"Error adding flight: {e}")
            return None

    def update_flight(self, flight):
        try:
            return self.DAL.update(flight)
        except Exception as e:
            logger.error(f"Error updating flight: {e}")
            return None

    def remove_flight(self, flight):
        try:
            return self.DAL.remove(flight)
        except Exception as e:
            logger.error(f"Error removing flight: {e}")
            return None
        

    def search_flights(self, query):
        """
        Search for flights by ID.
        """
        try:
            return self._dal.search(Flights, 'id', query)
        except Exception as e:
            logger.error(f"Error searching flights: {e}")
            return None

    def get_all_flights_sorted(self, sort_by):
        """
        Get all flights, sorted by a specific field.
        """
        try:
            return self._dal.get_all_sorted(Flights, sort_by)
        except Exception as e:
            logger.error(f"Error getting all flights sorted: {e}")
            return None
    


    def validate_flight(self, flight):
        """
        Validate a flight's data.
        """
        try:
            if flight.departure_time >= flight.landing_time:
                raise ValueError("A flight's departure time must be before its landing time.")
        except Exception as e:
            logger.error(f"Error validating flight: {e}")
            return None
