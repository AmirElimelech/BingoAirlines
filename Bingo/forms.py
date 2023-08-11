from django import forms
from .models import Users, Customers, Airline_Companies, Administrators
from django.core.validators import validate_email



class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'})
    )



class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'email', 'user_role', 'image']

    def __init__(self, *args, user_role=None, **kwargs):
        super(UsersForm, self).__init__(*args, **kwargs)
        if user_role:
            self.fields['user_role'].initial = user_role
            self.fields['user_role'].widget = forms.HiddenInput()   

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        return cleaned_data
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Users.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
    

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ['id', 'user_id']

class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrators
        exclude = ['id', 'user_id']

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if Administrators.objects.filter(user_id__username=username).exists():
            raise forms.ValidationError("Username already exists for an administrator.")
        return username

    

class AirlineCompanyForm(forms.ModelForm):
    class Meta:
        model = Airline_Companies
        exclude = ['id', 'user_id', 'logo']  # I excluded the 'logo' assuming you'll handle it separately. If not, you can remove it from the exclude list.

    def clean_iata_code(self):
        iata_code = self.cleaned_data.get("iata_code")
        if Airline_Companies.objects.filter(iata_code=iata_code).exists():
            raise forms.ValidationError("Airline with this IATA code already exists.")
        return iata_code

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Airline_Companies.objects.filter(name=name).exists():
            raise forms.ValidationError("Airline with this name already exists.")
        return name