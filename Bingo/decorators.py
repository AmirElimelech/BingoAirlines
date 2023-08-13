from functools import wraps
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        login_token = request.session.get('login_token')
        if not login_token or not login_token.get('user_id'):
            logger.info("User not logged in, redirecting to login page.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper




