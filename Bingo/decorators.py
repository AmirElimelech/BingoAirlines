
import logging
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.response import Response



logger = logging.getLogger(__name__)


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        login_token = request.session.get('login_token')
        if not login_token or not login_token.get('user_id'):
            logger.info("User not logged in, redirecting to login page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper



def check_permissions(*permission_classes):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            for permission_class in permission_classes:
                permission = permission_class()
                if permission.has_permission(request, None):
                    logger.info(f"Permission granted to user role {request.user.user_role.role_name} .")
                    return view_func(request, *args, **kwargs)
            logger.warning("Permission denied.")
            return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        return _wrapped_view
    return decorator
