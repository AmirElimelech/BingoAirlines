

# import logging


# logger = logging.getLogger(__name__)


# class LoginToken:
#     def __init__(self, user_id, user_role):
#         self.user_id = user_id
#         self.user_role = user_role

   
#     @staticmethod
#     def validate_login_token(request):
#         login_token_dict = request.session.get('login_token')
        
#         if not login_token_dict:
#             logger.error(f"Unauthorized access attempt by {request.user.username}")
#             raise PermissionError("Unauthorized access. Please login again.")
            
#         login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
#         user_id = login_token.user_id
        
#         if not user_id:
#             logger.info("Authentication expired. Please login again.")
#             raise PermissionError("Authentication expired. Please login again.")
        


#WORKINGGGGGGGGG BEFORREEEE ROLL TO IT IF NEEDED ! 
# import logging 
# from ..models import Users  , DAL # Importing the Users model

# logger = logging.getLogger(__name__)

# class LoginToken:
#     def __init__(self, user_id, user_role):
#         self.user_id = user_id
#         self.user_role = user_role

#     @staticmethod
#     def validate_login_token(request):
#         login_token_dict = request.session.get('login_token')
        
#         if not login_token_dict:
#             logger.error(f"Unauthorized access attempt by {request.user.username}")
#             raise PermissionError("Unauthorized access. Please login again.")
            
#         login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
#         user_id = login_token.user_id
        
#         if not user_id:
#             logger.info("Authentication expired. Please login again.")
#             raise PermissionError("Authentication expired. Please login again.")
        
#         # Set the user in the request after validating the token
#         user = Users.objects.get(id=user_id)
#         request.user = user

#         return login_token


import logging
from Bingo.models import DAL , Users # Adjust the import path as necessary

logger = logging.getLogger(__name__)

class LoginToken:
    def __init__(self, user_id, user_role):
        self.user_id = user_id
        self.user_role = user_role

    @staticmethod
    def validate_login_token(request):
        dal = DAL()  # Instantiate the DAL class
        
        login_token_dict = request.session.get('login_token')
        
        if not login_token_dict:
            logger.error(f"Unauthorized access attempt by {request.user.username}")
            raise PermissionError("Unauthorized access. Please login again.")
            
        login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
        user_id = login_token.user_id
        
        if not user_id:
            logger.info("Authentication expired. Please login again.")
            raise PermissionError("Authentication expired. Please login again.")
        
        # Set the user in the request after validating the token using DAL
        user = dal.get_by_id(Users, user_id)
        if not user:
            raise PermissionError("Invalid user from token. Please login again.")
        
        request.user = user

        return login_token


