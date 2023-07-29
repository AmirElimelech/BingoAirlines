
# from .customer_facade import CustomerFacade
# from .airline_facade import AirlineFacade
# from .administrator_facade import AdministratorFacade


# from django.contrib.auth.models import User
# from .facade_base import FacadeBase
# from django.contrib.auth.hashers import check_password
# from Bingo.models import Customers, Users
# from django.contrib.auth import authenticate
# from .facade_base import FacadeBase

# class AnonymousFacade(FacadeBase):

#     def login(self, request, username, password):
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 if user.user_role.role_name == 'Customer':
#                     return CustomerFacade(), user.id
#                 elif user.user_role.role_name == 'Airline':
#                     return AirlineFacade(), user.id
#                 elif user.user_role.role_name == 'Administrator':
#                     return AdministratorFacade(), user.id
#         raise ValueError('Invalid credentials')

#     def add_customer(self, customer):
#         # assuming 'customer' is a dictionary containing the details of the customer
#         user = User.objects.create_user(username=customer['user']['username'], password=customer['user']['password'])
#         customer['user_id'] = user.id
#         return self._dal.add(Customers, **customer)
    






# ------------------------------------------------------------------------------------------------------------------------------

from .customer_facade import CustomerFacade
from .airline_facade import AirlineFacade
from .administrator_facade import AdministratorFacade
from .facade_base import FacadeBase
from models import Customers, Users
from werkzeug.security import check_password_hash
import logging

logger = logging.getLogger(__name__)

class AnonymousFacade(FacadeBase):

    def login(self, username, password):
        user = self.DAL.get_user_by_username(username)
        if user is not None and check_password_hash(user.password, password):
            if user.user_role.role_name == 'Customer':
                return CustomerFacade(user)
            elif user.user_role.role_name == 'Airline':
                return AirlineFacade(user)
            elif user.user_role.role_name == 'Administrator':
                return AdministratorFacade(user)
        else:
            logger.warning(f"Invalid login attempt for username: {username}")
        return None

    def add_customer(self, customer):
        try:
            return self.DAL.add(Customers, **customer)
        except Exception as e:
            logger.error(f"Error adding customer: {e}")
            return None


