from .customer_facade import CustomerFacade
from .airline_facade import AirlineFacade
from .administrator_facade import AdministratorFacade
from .facade_base import FacadeBase
from models import Customers, Users
from authentication.models import LoginToken


class AnonymousFacade(FacadeBase):
    def login(self, username, password):
        user = self.DAL.get_user_by_username(username)
        if user is not None and user.check_password(password):
            if user.user_role.role_name == 'Customer':
                # Create the LoginToken object with user information
                login_token = LoginToken(name=user.username, role='customer')
                return CustomerFacade(login_token), user.id
            elif user.user_role.role_name == 'Airline':
                # Create the LoginToken object with user information
                login_token = LoginToken(name=user.username, role='airline')
                return AirlineFacade(login_token), user.id
            elif user.user_role.role_name == 'Administrator':
                # Create the LoginToken object with user information
                login_token = LoginToken(name=user.username, role='administrator')
                return AdministratorFacade(login_token), user.id
        return None

    def add_customer(self, customer):
        user = Users.objects.create_user(username=customer['user']['username'], password=customer['user']['password'])
        customer['user_id'] = user.id
        return self.DAL.add(Customers, **customer)
