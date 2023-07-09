from .facade_base import FacadeBase
from Bingo.models import Tickets, Customers

class CustomerFacade(FacadeBase):

    def update_customer(self, customer):
        return self._dal.update(Customers, **customer)

    def add_ticket(self, ticket):
        return self._dal.add(Tickets, **ticket)

    def remove_ticket(self, ticket):
        return self._dal.remove(ticket)

    def get_my_tickets(self, customer_id):
        return self._dal.get_tickets_by_customer(customer_id)
