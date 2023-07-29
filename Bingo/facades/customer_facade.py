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
import logging

logger = logging.getLogger(__name__)

class CustomerFacade(FacadeBase):
    def __init__(self, user):
        super().__init__()
        self.user = user

    def update_customer(self, customer):
        try:
            return self.DAL.update(self.user.customer, **customer)
        except Exception as e:
            logger.error(f"Error updating customer: {e}")
            return None

    def add_ticket(self, ticket):
        try:
            return self.DAL.add(Tickets, **ticket)
        except Exception as e:
            logger.error(f"Error adding ticket: {e}")
            return None


    def remove_ticket(self, ticket):
        try:
            return self.DAL.remove(ticket)
        except Exception as e:
            logger.error(f"Error removing ticket: {e}")
            return None

    def get_my_tickets(self):
        try:
            return self.DAL.get_tickets_by_customer(self.user.customer.id)
        except Exception as e:
            logger.error(f"Error getting my tickets: {e}")
            return None
