

import logging
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.response import Response
from .models import Users

# Set up logging
logger = logging.getLogger(__name__)

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        login_token = request.session.get('login_token')
        
        if not login_token:
            logger.info("login_token is not found in the session.")
            
        if not login_token or not login_token.get('user_id'):
            logger.info("User not logged in, redirecting to login page.")
            return redirect('login')
        
        # Fetch the user based on the user_id from the session
        try:
            user_instance = Users.objects.get(id=login_token['user_id'])
            request.user = user_instance  # Attach the user instance to the request
            user_role_str = user_instance.user_role.role_name if hasattr(user_instance, 'user_role') else 'No role'
        except Users.DoesNotExist:
            user_role_str = 'User not found'
        
        logger.info(f"User is logged in with role {user_role_str}")
        return view_func(request, *args, **kwargs)

    
    return wrapper

def check_permissions(*permission_classes):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()
                logger.info(f"Checking permission for: {permission_class.__name__}")
                
                if hasattr(request, 'user') and permission.has_permission(request, request.user):  
                    logger.info(f"Permission {permission_class.__name__} granted to user role {request.user.user_role}.")
                    return view_func(request, *args, **kwargs)
            
            logger.warning("All permission checks failed. Permission denied.")
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view

    return decorator
