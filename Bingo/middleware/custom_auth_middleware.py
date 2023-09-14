
import logging
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from Bingo.backends import CustomUserAuthBackend

logger = logging.getLogger(__name__)

class CustomAuthMiddleware(MiddlewareMixin):
    """
        Middleware for custom user authentication.

        This middleware integrates a custom authentication method using `CustomUserAuthBackend`. 
        It attempts to authenticate users based on a 'login_token' stored in the session. 
        If the user is authenticated successfully, they are attached to the request object. 
        Otherwise, an AnonymousUser is attached to the request.
    """

    def process_request(self, request):

        """
        Process the incoming request to handle custom user authentication.

        """

        logger.debug("CustomAuthMiddleware triggered")
        

        backend = CustomUserAuthBackend()
        login_token = request.session.get('login_token')
        if login_token:
            """
            If a 'login_token' is found in the session, use the custom authentication 
            backend to authenticate the user based on the user_id stored in the 'login_token'.
            """
            user_instance = backend.authenticate(request=request, user_id=login_token.get('user_id'))
        else:
            user_instance = None
           
        request.user = user_instance if user_instance else AnonymousUser()
        logger.debug(f" Setting request.user to {request.user} with role {request.user.user_role.role_name if hasattr(request.user, 'user_role') else 'No role'}")
    


