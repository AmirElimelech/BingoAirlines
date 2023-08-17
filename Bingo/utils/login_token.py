import logging

logger = logging.getLogger(__name__)


class LoginToken:
    def __init__(self, user_id, user_role):
        self.user_id = user_id
        self.user_role = user_role

    # @staticmethod
    # def validate_login_token(self, login_token):
    #     user_id = login_token.user_id if isinstance(login_token, LoginToken) else login_token.get('user_id', None)
    #     if login_token is None or user_id is None:
    #         logging.info("Authentication expired. Please login again.")
    #         raise PermissionError("Authentication expired. Please login again.")


    @staticmethod
    def validate_login_token(request):
        login_token_dict = request.session.get('login_token')
        
        if not login_token_dict:
            logger.error(f"Unauthorized access attempt by {request.user.username}")
            raise PermissionError("Unauthorized access. Please login again.")
            
        login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
        user_id = login_token.user_id
        
        if not user_id:
            logger.info("Authentication expired. Please login again.")
            raise PermissionError("Authentication expired. Please login again.")
        
        return login_token
