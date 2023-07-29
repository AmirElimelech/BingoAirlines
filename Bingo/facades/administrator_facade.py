# from .facade_base import FacadeBase
# from Bingo.models import Customers, Airline_Companies, Administrators

# class AdministratorFacade(FacadeBase):

#     def get_all_customers(self):
#         return self.dal.get_all(Customers)

#     def add_airline(self, airline):
#         return self.dal.add(Airline_Companies, **airline)

#     def add_customer(self, customer):
#         user = self.create_new_user(customer['user'])
#         customer['user_id'] = user.id
#         return self.dal.add(Customers, **customer)

#     def add_administrator(self, administrator):
#         user = self.create_new_user(administrator['user'])
#         administrator['user_id'] = user.id
#         return self.dal.add(Administrators, **administrator)

#     def remove_airline(self, airline):
#         return self.dal.remove(airline)

#     def remove_customer(self, customer):
#         return self.dal.remove(customer)

#     def remove_administrator(self, administrator):
#         return self.dal.remove(administrator)


# ------------------------------------------------------------------------------------------------------------------------------


from .facade_base import FacadeBase
from models import Customers, Administrators, Airline_Companies
import logging

logger = logging.getLogger(__name__)

class AdministratorFacade(FacadeBase):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def get_all_customers(self):
        try:
            return self.DAL.get_all(Customers)
        except Exception as e:
            logger.error(f"Error getting all customers: {e}")
            return None

    def add_airline(self, airline):
        try:
            return self.DAL.add(Airline_Companies, **airline)
        except Exception as e:
            logger.error(f"Error adding airline: {e}")
            return None

    def add_customer(self, customer):
        try:
            return self.DAL.add(Customers, **customer)
        except Exception as e:
            logger.error(f"Error adding customer: {e}")
            return None

    def add_administrator(self, administrator):
        try:
            return self.DAL.add(Administrators, **administrator)
        except Exception as e:
            logger.error(f"Error adding administrator: {e}")
            return None

    def remove_airline(self, airline):
        try:
            return self.DAL.remove(airline)
        except Exception as e:
            logger.error(f"Error removing airline: {e}")
            return None

    def remove_customer(self, customer):
        try:
            return self.DAL.remove(customer)
        except Exception as e:
            logger.error(f"Error removing customer: {e}")
            return None

    def remove_administrator(self, administrator):
        try:
            return self.DAL.remove(administrator)
        except Exception as e:
            logger.error(f"Error removing administrator: {e}")
            return None
