# from django import forms
# from .models import Users
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# class UsersForm(forms.ModelForm):
#     class Meta:
#         model = Users
#         fields = ['id', 'username', 'password', 'email', 'user_role', 'image']




# class CustomUserCreationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     user_role = forms.ChoiceField(choices=[
#         ('customer', 'Customer'),
#         ('airline_company', 'Airline Company'),
#         ('administrator', 'Administrator'),
#     ])
#     image = forms.ImageField()

#     class Meta:
#         model = User
#         fields = UserCreationForm.Meta.fields + ('email', 'user_role', 'image',)

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data['email']
#         # Add additional fields as needed
#         if commit:
#             user.save()
#         return user


# from django import forms
# from django.contrib.auth.hashers import make_password
# from .models import Users , User_Roles

# class CustomUserRegistrationForm(forms.ModelForm):
#     id = forms.CharField(max_length=9, required=True)
#     email = forms.EmailField(required=True)
#     user_role = forms.ChoiceField(choices=[
#         ('Customer', 'customer'),
#         ('Airline_company', 'airline Company'),
#         ('Administrator', 'administrator'),
#     ])
#     image = forms.ImageField()

#     class Meta:
#         model = Users
#         fields = ('id', 'username', 'password', 'email', 'user_role', 'image',)


#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.password = make_password(self.cleaned_data['password'])
#         user.user_role = User_Roles.objects.get(role_name=self.cleaned_data['user_role'])
#         if commit:
#             user.save()
#         return user



from django import forms
from django.contrib.auth.hashers import make_password
from .models import Users

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'email', 'user_role', 'image']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
