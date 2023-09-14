
from django.contrib.auth.backends import BaseBackend
from .models import Users

class CustomUserAuthBackend(BaseBackend):

    def authenticate(self, request, user_id=None, **kwargs):
        try:
            user = Users.objects.get(id=user_id)
            return user
        except Users.DoesNotExist:
            return None
            
    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None
