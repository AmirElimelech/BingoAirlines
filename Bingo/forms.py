from django import forms
import datetime , logging
from django.core.validators import validate_email
from .models import Users, Customers, Airline_Companies, Administrators




logger = logging.getLogger(__name__)

class UsersForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['id', 'username', 'password', 'email', 'user_role', 'image']

    def __init__(self, *args, user_role=None, **kwargs):
        try:
            super(UsersForm, self).__init__(*args, **kwargs)
            if user_role:
                self.fields['user_role'].initial = user_role
                self.fields['user_role'].widget = forms.HiddenInput()
        except Exception as e:
            logger.error(f"Error initializing UsersForm: {e}")
            raise e

    def clean(self):
        try:
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            return cleaned_data
        except Exception as e:
            logger.error(f"Error during cleaning data in UsersForm: {e}")
            raise e
    
    def clean_email(self):
        try:
            email = self.cleaned_data.get("email")
            if Users.objects.filter(email=email).exists():
                raise forms.ValidationError("Email already exists.")
            validate_email(email)
            return email
        except forms.ValidationError as ve:
            logger.warning(f"ValidationError in clean_email of UsersForm: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Unexpected error in clean_email of UsersForm: {e}")
            raise e

    def clean_username(self):
        try:
            username = self.cleaned_data.get("username")
            if Users.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already exists.")
            return username
        except forms.ValidationError as ve:
            logger.warning(f"ValidationError in clean_username of UsersForm: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Unexpected error in clean_username of UsersForm: {e}")
            raise e
    


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customers
        exclude = ['id', 'user_id']

    def clean(self):
        try:
            cleaned_data = super().clean()
            return cleaned_data
        except Exception as e:
            logger.error(f"Error during cleaning data in CustomerForm: {e}")
            raise e




class AdministratorForm(forms.ModelForm):
    class Meta:
        model = Administrators
        exclude = ['id', 'user_id']

    def clean(self):
        try:
            cleaned_data = super().clean()
            return cleaned_data
        except Exception as e:
            logger.error(f"Error during cleaning data in AdministratorForm: {e}")
            raise e

   
    


class AirlineCompanyForm(forms.ModelForm):
    class Meta:
        model = Airline_Companies
        exclude = ['id', 'user_id']

    def clean(self):
        try:
            cleaned_data = super().clean()
            return cleaned_data
        except Exception as e:
            logger.error(f"Error during cleaning data in AirlineCompanyForm: {e}")
            raise e

    def clean_iata_code(self):
        try:
            iata_code = self.cleaned_data.get("iata_code")
            if Airline_Companies.objects.filter(iata_code=iata_code).exists():
                raise forms.ValidationError("Airline with this IATA code already exists.")
            return iata_code
        except forms.ValidationError as ve:
            logger.warning(f"ValidationError in clean_iata_code of AirlineCompanyForm: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Unexpected error in clean_iata_code of AirlineCompanyForm: {e}")
            raise e

    def clean_name(self):
        try:
            name = self.cleaned_data.get("name")
            if Airline_Companies.objects.filter(name=name).exists():
                raise forms.ValidationError("Airline with this name already exists.")
            return name
        except forms.ValidationError as ve:
            logger.warning(f"ValidationError in clean_name of AirlineCompanyForm: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"Unexpected error in clean_name of AirlineCompanyForm: {e}")
            raise e


class SearchForm(forms.Form):
    logging.info("Starting the clean method of SearchForm.")
    numAdults = forms.IntegerField(min_value=1, initial=1 , label='Adults')
    numChildren = forms.IntegerField(min_value=0, initial=0 , label='Children')
    cabinType = forms.ChoiceField(choices=[('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First')] , label='Cabin Type')
    currencyCode = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('ILS', 'ILS')] , label='Currency')
    originLocationCode = forms.CharField(label='Flying From') 
    destinationLocationCode = forms.CharField(label='Flying To')
    departureDate1 = forms.DateField(label='Departure Date')
    flightType = forms.ChoiceField(choices=[('OneWay', 'One Way'), ('Return', 'Return Flight')] , label='Flight Type')
    departureDate2 = forms.DateField(required=False , label='Return Date')

    def clean(self):
        cleaned_data = super().clean()
        departureDate1 = cleaned_data.get('departureDate1')
        departureDate2 = cleaned_data.get('departureDate2')
        originLocationCode = cleaned_data.get('originLocationCode')
        destinationLocationCode = cleaned_data.get('destinationLocationCode')
        cabinType = cleaned_data.get('cabinType')
        numAdults = cleaned_data.get('numAdults')
        numChildren = cleaned_data.get('numChildren')
        currencyCode = cleaned_data.get('currencyCode')


        # Check that all fields are filled

        # Check that departure date is not in the past
        if departureDate1 and departureDate1 < datetime.date.today():
            logging.error("Error: Departure date is in the past.")
            self.add_error('departureDate1', 'Departure date cannot be in the past.')

        # Check that return date is not before the departure date
        if departureDate2 and departureDate1 and departureDate2 < departureDate1:
            logging.error("Error: Return date is before the departure date.")
            self.add_error('departureDate2', 'Return date cannot be before the departure date.')

        # Check that origin and destination are not the same
        if originLocationCode and destinationLocationCode and originLocationCode == destinationLocationCode:
            logging.error("Error: Origin and destination are the same.")
            self.add_error('destinationLocationCode', 'You cannot select the same airport for departure and arrival.')

        # Check cabin type
        if cabinType not in ['ECONOMY', 'BUSINESS', 'FIRST']:
            logging.error("Error: Invalid cabin type selected.")
            self.add_error('cabinType', 'Invalid cabin type selected.')


        # Validate number of passengers
        if numAdults and numAdults > 9:
            logging.error("Error: Too many adults selected.")
            self.add_error('numAdults', 'You cannot book for more than 9 adults at once.')
        if numChildren and numChildren > 9:
            logging.error("Error: Too many children selected.")
            self.add_error('numChildren', 'You cannot book for more than 9 children at once.')


        # Validate currency code
        if currencyCode not in ['USD', 'EUR', 'GBP', 'ILS']:
            logging.error("Error: Invalid currency code selected.")
            self.add_error('currencyCode', 'Invalid currency code selected.')


        return cleaned_data