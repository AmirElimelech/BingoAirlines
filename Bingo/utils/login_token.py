
import logging
from Bingo.models import DAL, Users 







logger = logging.getLogger(__name__)





class LoginToken:
    def __init__(self, user_id, user_role):
        """
        Constructor for the LoginToken class.

        Parameters:
        - user_id (int): The ID of the user.
        - user_role (str): The role of the user (e.g., 'administrator', 'customer' , 'airline company' ).
        """
        self.user_id = user_id
        self.user_role = user_role

    @staticmethod
    def validate_login_token(request):
        """
        Validate the login token present in the session.

        This method checks if there's a valid login token in the session. If found, it ensures
        the user associated with that token exists in the system. Once validated, the user 
        instance is attached to the request for further processing.

        Parameters:
        - request: The Django request object.

        Returns:
        - LoginToken: A validated LoginToken object.

        Raises:
        - PermissionError: If there's an issue with the login token or if the associated user doesn't exist.
        """

        try:
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

        except Exception as e:
            logger.error(f"Error while validating login token: {str(e)}")
            raise PermissionError("An error occurred while validating the login token.")


