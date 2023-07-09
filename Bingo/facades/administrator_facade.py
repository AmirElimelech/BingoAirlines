from .facade_base import FacadeBase
from Bingo.models import Customers, Airline_Companies, Administrators

class AdministratorFacade(FacadeBase):

    def get_all_customers(self):
        return self.dal.get_all(Customers)

    def add_airline(self, airline):
        return self.dal.add(Airline_Companies, **airline)

    def add_customer(self, customer):
        user = self.create_new_user(customer['user'])
        customer['user_id'] = user.id
        return self.dal.add(Customers, **customer)

    def add_administrator(self, administrator):
        user = self.create_new_user(administrator['user'])
        administrator['user_id'] = user.id
        return self.dal.add(Administrators, **administrator)

    def remove_airline(self, airline):
        return self.dal.remove(airline)

    def remove_customer(self, customer):
        return self.dal.remove(customer)

    def remove_administrator(self, administrator):
        return self.dal.remove(administrator)
