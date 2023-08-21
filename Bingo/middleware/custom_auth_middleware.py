
# import logging
# from ..models import DAL, Users  # Adjust the import path as necessary
# from django.contrib.auth.models import AnonymousUser

# logger = logging.getLogger(__name__)

# class CustomAuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):

#         if request.path.startswith('/admin/'):
#             return self.get_response(request)
        
#         # Default to AnonymousUser
#         request.user = AnonymousUser()
        
        
#         # Check for a login token in the session
#         login_token_dict = request.session.get('login_token')
#         if login_token_dict:
#             user_id = login_token_dict.get('user_id')
#             if user_id:
#                 # Retrieve the user from the database using DAL
#                 dal_instance = DAL()
#                 user = dal_instance.get_by_id(Users, user_id)
#                 if user:
#                     request.user = user
#                     logger.info(f"User {user.username} authenticated via token.")
#                     logger.info(f"Is authenticated: {request.user.is_authenticated}")
#                 else:
#                     logger.error(f"User with ID {user_id} from token not found in database.")
#             else:
#                 logger.error("Login token present but user_id missing.")
#         else:
#             logger.info("No login token found in the session.")

#         response = self.get_response(request)
#         return response




import logging
from ..models import DAL, Users  # Adjust the import path as necessary
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow requests to the admin panel
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Default to AnonymousUser
        request.user = AnonymousUser()
        
        # Check for a login token in the session
        login_token_dict = request.session.get('login_token')
        if login_token_dict:
            user_id = login_token_dict.get('user_id')
            if user_id:
                # Retrieve the user from the database using DAL
                dal_instance = DAL()
                user = dal_instance.get_by_id(Users, user_id)
                if user:
                    request.user = user
                    logger.info(f"User {user.username} authenticated via token.")
                    logger.info(f"Is authenticated: {request.user.is_authenticated}")
                    print(request.session.get('login_token'))

                else:
                    logger.error(f"User with ID {user_id} from token not found in database.")
            else:
                logger.error("Login token present but user_id missing.")
        else:
            logger.info("No login token found in the session.")

        response = self.get_response(request)
        
        return response