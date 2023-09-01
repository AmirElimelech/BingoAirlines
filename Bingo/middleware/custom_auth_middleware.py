
import logging
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin
from Bingo.backends import CustomUserAuthBackend

logger = logging.getLogger(__name__)

class CustomAuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        logger.debug("1 CustomAuthMiddleware triggered")
        
        # If request path is for the admin panel or static files, bypass custom authentication.
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return None
        

        backend = CustomUserAuthBackend()
        login_token = request.session.get('login_token')
        if login_token:
            user_instance = backend.authenticate(request=request, user_id=login_token.get('user_id'))
        else:
            user_instance = None
           
        request.user = user_instance if user_instance else AnonymousUser()
        logger.debug(f" Setting request.user to {request.user} with role {request.user.user_role.role_name if hasattr(request.user, 'user_role') else 'No role'}")
    


