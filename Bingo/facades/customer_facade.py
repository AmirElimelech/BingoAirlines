# from .facade_base import FacadeBase
# from Bingo.models import Tickets, Customers

# class CustomerFacade(FacadeBase):

#     def update_customer(self, customer):
#         return self._dal.update(Customers, **customer)

#     def add_ticket(self, ticket):
#         return self._dal.add(Tickets, **ticket)

#     def remove_ticket(self, ticket):
#         return self._dal.remove(ticket)

#     def get_my_tickets(self, customer_id):
#         return self._dal.get_tickets_by_customer(customer_id)


# ------------------------------------------------------------------------------------------------------------------------------


from .facade_base import FacadeBase
from models import Customers, Tickets

class CustomerFacade(FacadeBase):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def update_customer(self, customer):
        return self.DAL.update(self.user.customer, **customer)

    def add_ticket(self, ticket):
        return self.DAL.add(Tickets, **ticket)

    def remove_ticket(self, ticket):
        return self.DAL.remove(ticket)

    def get_my_tickets(self):
        return self.DAL.get_tickets_by_customer(self.user.customer.id)
