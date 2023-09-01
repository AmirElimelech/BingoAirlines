# from django.contrib.auth.backends import BaseBackend
# from .models import Users

# class CustomUserAuthBackend(BaseBackend):
#     def authenticate(self, request, user_id=None, **kwargs):
#         try:
#             return Users.objects.get(id=user_id)
#         except Users.DoesNotExist:
#             return None

#     def get_user(self, user_id):
#         try:
#             return Users.objects.get(pk=user_id)
#         except Users.DoesNotExist:
#             return None


# from django.contrib.auth.backends import BaseBackend
# from .models import Users








# from django.contrib.auth.backends import BaseBackend
# from .models import Users


# class CustomUserAuthBackend(BaseBackend):
#     def authenticate(self, request, user_id=None, **kwargs):
#         print(f"backend -1- Entering authenticate method")
        
#         print(f"backend -2- Before trying to get user by ID")
#         try:
#             user = Users.objects.get(id=user_id)
#             print(f"backend -3- User found by ID:", user_id)
#             return user
#         except Users.DoesNotExist:
#             print(f"backend -4- User with ID", user_id, "does not exist")
#             return None
#         finally:
#             print(f"backend -5- Exiting the try-except block in authenticate method")
            
    
#     def get_user(self, user_id):
#         print(f"backend -6- Entering get_user method")
        
#         print(f"backend -7- Before trying to get user by PK")
#         try:
#             user = Users.objects.get(pk=user_id)
#             print(f"backend -8- User found by PK:", user_id)
#             return user
#         except Users.DoesNotExist:
#             print(f"backend -9- User with PK", user_id, "does not exist")
#             return None
#         finally:
#             print(f"backend -10- Exiting the try-except block in get_user method")
            





# try it : 
from django.contrib.auth.backends import BaseBackend
from .models import Users

class CustomUserAuthBackend(BaseBackend):

    def authenticate(self, request, user_id=None, **kwargs):
        try:
            user = Users.objects.get(id=user_id)
            return user
        except Users.DoesNotExist:
            return None
            
    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
