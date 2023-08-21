
# from .facade_base import FacadeBase
# from ..models import Customers, Users 
# from django.contrib.auth.hashers import check_password
# from django.core.exceptions import ValidationError
# from ..utils.login_token import LoginToken





# class AnonymousFacade(FacadeBase):


#     def login(self, request, username, password):

#         user = self.DAL.get_user_by_username(username)
        


#         if user is None:
#             raise ValidationError("User not found")
#         if not check_password(password, user.password):
#             raise ValidationError("Incorrect password")
        

#         request.user = user
        

        
#         # Determine the role of the user
#         role = None
#         if user.user_role.role_name == 'Customer':
#             role = 'customer'
#         elif user.user_role.role_name == 'Airline Company':
#             role = 'airline company'
#         elif user.user_role.role_name == 'Administrator':
#             role = 'administrator'

#         login_token = LoginToken(user.id, role)

#         return login_token



    # def add_customer(self, customer):
                
    #     user_instance = Users.objects.get(id=customer["user_id"])
    #     customer["user_id"] = user_instance

    #     return self.DAL.add(Customers, **customer)



from .facade_base import FacadeBase
from ..models import Customers, Users 
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from ..utils.login_token import LoginToken
import logging

logger = logging.getLogger(__name__)


class AnonymousFacade(FacadeBase):
    def __init__(self, request, login_token: LoginToken=None):
        super().__init__(request, login_token)



    def login(self, username, password):
        user = self.DAL.get_user_by_username(username)

        if user is None:
            raise ValidationError("User not found")
        if not check_password(password, user.password):
            raise ValidationError("Incorrect password")
        
        self.request.user = user

        # Determine the role of the user
        role = None
        if user.user_role.role_name == 'Customer':
            role = 'customer'
        elif user.user_role.role_name == 'Airline Company':
            role = 'airline company'
        elif user.user_role.role_name == 'Administrator':
            role = 'administrator'

        login_token = LoginToken(user.id, role)

        return login_token

    def add_customer(self, customer):
        user_instance = self.DAL.get_by_id(Users, customer["user_id"])
        customer["user_id"] = user_instance
        return self.DAL.add(Customers, **customer)