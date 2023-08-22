
import logging
from ..models import DAL, Users  
from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)

class CustomAuthMiddleware:

    """
    Custom authentication middleware for BingoAirlines project.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Allow requests to the admin panel ( added this to be able to login to admin panel because i i've added my own 
        # Middleware )
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Default to AnonymousUser if no user is logged in
        request.user = AnonymousUser()
        
        # Check for a login token in the session
        login_token_dict = request.session.get('login_token')
        if login_token_dict:
            # Extract the user_id from the login token
            user_id = login_token_dict.get('user_id')

            # Check if the user_id is present in the login token
            if user_id:

                # Retrieve the user from the database using DAL
                dal_instance = DAL()
                user = dal_instance.get_by_id(Users, user_id)
                # Check if the user exists in the database
                if user:
                    # Set the user in the request object to the user retrieved from the database
                    request.user = user
                    logger.info(f"User {user.username} authenticated via token.")
                    logger.info(f"{user.username} Is authenticated ? : {request.user.is_authenticated}")
                    

                else:
                    logger.error(f"User with ID {user_id} from token not found in database.")
            else:
                logger.error("Login token present but user_id missing.")
        else:
            logger.info("No login token found in the session.")

        response = self.get_response(request)
        
        return response