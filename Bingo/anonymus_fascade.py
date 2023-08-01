from .models import Users
from django.core.exceptions import ObjectDoesNotExist
from .models import LoginToken

class CustomerFacade:
    def __init__(self, user):
        self.user = user

    def some_customer_function(self):
        tokens = self.user.get_login_token()
        if tokens:
            for token in tokens:
                if not token or token.role != 'customer':
                    return "Unauthorized"
                else:
                    return "authorized"
        

class AirlineFacade:
    def __init__(self, user):
        self.user = user

    def some_airline_function(self):
        tokens = self.user.get_login_token()
        if tokens:
            for token in tokens:
                if not token or token.role != 'airline':
                    return "Unauthorized"
                else:
                    return "authorized"
        

class AdminFacade:
    def __init__(self, user):
        self.user = user

    def some_admin_function(self):
        tokens = self.user.get_login_token()
        if tokens:
            for token in tokens:
                if not token or token.role != 'admin':
                    return "Unauthorized"
                else:
                    return "authorized"
        
class AnonymousFacade:
    def login(self, username, password):
        try:
            users = Users.objects.filter(username=username, password=password)
            
            user=users[0]
            login_token = LoginToken(name=user.username, role=user.user_role.role_name)
            login_token.save()
            if user.user_role.role_name == 'customer':
                return CustomerFacade(user)
            elif user.user_role.role_name == 'airline':
                return AirlineFacade(user)
            elif user.user_role.role_name == 'admin':
                return AdminFacade(user)
            else:
                return None

        except ObjectDoesNotExist:
            return None
