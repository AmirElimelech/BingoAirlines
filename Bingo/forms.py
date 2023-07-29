from django import forms
from .models import Users

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'email', 'user_role', 'image']
