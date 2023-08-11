from datetime import timedelta
from django.db import models
import requests
from django.core import validators
from io import BytesIO
from django.core.files.base import ContentFile
import urllib
from django.core.files import File
import logging
from django.core.validators import MinValueValidator
import string , random
from django.db import models
from django.utils import timezone
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.core.validators import MinValueValidator
import string
import random
import re

logger = logging.getLogger(__name__)



class Flights(models.Model):
    id = models.BigAutoField(primary_key=True)
    airline_company_id = models.ForeignKey('Airline_Companies', to_field='iata_code', on_delete=models.CASCADE)
    origin_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='origin_flights')
    destination_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='destination_flights')
    departure_time = models.DateTimeField(null=False)
    landing_time = models.DateTimeField(null=False)
    remaining_tickets = models.IntegerField(null=False, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'Flight {self.id}'
    
    class Meta:
        verbose_name_plural = "Flights"





# Countries model represents different countries
class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

        
    
        


# Tickets model represents individual flight tickets
class Tickets(models.Model):
    id = models.BigAutoField(primary_key=True)
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
    customer_id = models.ForeignKey('Customers', on_delete=models.CASCADE)

    def __str__(self):
        return f'Ticket {self.id}'
    
    class Meta:
        verbose_name_plural = "Tickets"
    



class Airline_Companies(models.Model):
    iata_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, unique=True)
    logo = models.ImageField(upload_to='airline_logos/', default='/airline_logos/airplanelogo.png', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Airline Companies"


    def save(self, *args, **kwargs):
        logger.info(f"Attempting to save Airline_Companies instance with iata_code: {self.iata_code}")

        if self.iata_code and not self.logo:
            # Download the logo from the URL
            url = f'https://content.r9cdn.net/rimg/provider-logos/airlines/v/{self.iata_code}.png?crop=false&width=100&height=100'
            try:
                response = urllib.request.urlopen(url)
                if response.status == 200:
                    # Save the logo to the ImageField
                    filename = f'{self.iata_code}.png'
                    self.logo.save(filename, File(response), save=False)
                    logger.info(f"Downloaded and saved logo for {self.iata_code} from {url}")
                else:
                    self.logo = 'airplanelogo.png'
                    logger.warning(f"Received status {response.status} when trying to download logo from {url}")
            except Exception as e:
                self.logo = 'airplanelogo.png'
                logger.error(f"Error when trying to download logo from {url}: {e}")

        # If logo wasn't specified and couldn't be downloaded, use the default logo
        if not self.logo:
            self.logo = 'airplanelogo.png'
        
        super().save(*args, **kwargs)
        logger.info(f"Saved Airline_Companies instance with iata_code: {self.iata_code}")

  
    @property
    def image_url(self):
        if self.logo:
            return self.logo.url
        else:
            return '/media/airplanelogo.png" style="width: 100px; height: 100px;"'

        

# Customers model represents individual customers
class Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    address = models.TextField(null=False)
    phone_no = models.CharField(max_length=15, unique=True, null=False)
    credit_card_no = models.CharField(max_length=16, unique=False, null=False)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name_plural = "Customers"
    
    # Method to retrieve the image URL of the customer's profile picture
    @property
    def image_url(self):
        try:
            url = self.user_id.image.url
        except:
            url = ''
        return url
    
    
    # Method to retrieve a masked version of the customer's credit card number leaving only the last 4 digits
    @property
    def masked_credit_card(self):
        return '*' * (len(self.credit_card_no) - 4) + self.credit_card_no[-4:]
    






def validate_password_strength(value):
    if len(value) < 6 or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", value):
        raise validators.ValidationError("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")


def validate_nine_digits(value):
    if len(str(value)) != 9:
        raise validators.ValidationError("ID must be exactly 9 digits long.")


# Users model represents individual user accounts
class Users(models.Model):
    id = models.CharField(max_length=9, primary_key=True, validators=[validate_nine_digits])
    username = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False , validators=[validate_password_strength])
    email = models.EmailField(max_length=255, unique=True, null=False)
    user_role = models.ForeignKey('User_Roles', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/', default='/users/defaultuser.png', null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name_plural = "Users"


    # Method to retrieve the image URL of the user's profile picture if none exists returns default image
    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

# User_Roles model represents different user roles ()
class User_Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.role_name
    
    class Meta:
        verbose_name_plural = "User Roles"
    

# Administrators model represents different administrators
class Administrators(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name_plural = "Administrators"



class Airport(models.Model):
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    



class DAL:
    def get_by_id(self, model, id):
        try:
            return model.objects.get(id=id)
        except model.DoesNotExist:
            return None

    def get_all(self, model):
        try:
            return model.objects.all()
        except Exception as e:
            return None

    def add(self, model, **kwargs):
        try:
            instance = model.objects.create(**kwargs)
            if instance:
                logger.info(f"Successfully created {model.__name__} instance: {instance}")
                return instance
            else:
                logger.error(f"Failed to create {model.__name__} instance with kwargs: {kwargs}")
                return None
        except Exception as e:
            logger.error(f"Error creating {model.__name__} instance with kwargs: {kwargs}. Error: {str(e)}")
            return None

   





    def update(self, instance, **kwargs):
        try:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except Exception as e:
            return None

    def add_all(self, model, list_of_dicts):
        try:
            return model.objects.bulk_create([model(**kwargs) for kwargs in list_of_dicts])
        except Exception as e:
            return None

    def remove(self, instance):
        try:
            instance.delete()
        except Exception as e:
            return None

    # Additional methods
    def getAirlinesByCountry(self, country_id):
        try:
            return Airline_Companies.objects.filter(country_id=country_id)
        except Exception as e:
            return None

    def getFlightsByOriginCountryId(self, country_id):
        try:
            return Flights.objects.filter(origin_id=country_id)
        except Exception as e:
            return None

    def getFlightsByDestinationCountryId(self, country_id):
        try:
            return Flights.objects.filter(destination_id=country_id)
        except Exception as e:
            return None

    def getFlightsByDepartureDate(self, date):
        try:
            return Flights.objects.filter(departure_date=date)
        except Exception as e:
            return None

    def getFlightsByLandingDate(self, date):
        try:
            return Flights.objects.filter(landing_date=date)
        except Exception as e:
            return None

    def getFlightsByCustomer(self, customer):
        try:
            return Flights.objects.filter(customer=customer)
        except Exception as e:
            return None
    
    def get_airline_by_username(self, _username):
        try:
            return Airline_Companies.objects.get(user__username=_username)
        except Airline_Companies.DoesNotExist:
            return None

    def get_customer_by_username(self, _username):
        try:
            return Customers.objects.get(user__username=_username)
        except Customers.DoesNotExist:
            return None

    def get_user_by_username(self, _username):
        try:
            return Users.objects.get(username=_username)
        except Users.DoesNotExist:
            return None

    def get_flights_by_parameters(self, _origin_country_id, _destination_country_id, _date):
        try:
            return Flights.objects.filter(
                origin_id=_origin_country_id,
                destination_id=_destination_country_id,
                departure_date=_date
            )
        except Exception as e:
            return None

    def get_flights_by_airline_id(self, _airline_id):
        try:
            return Flights.objects.filter(airline_company_id=_airline_id)
        except Exception as e:
            return None

    def get_arrival_flights(self, _country_id):
        try:
            next_12_hours = timezone.now() + timedelta(hours=12)
            return Flights.objects.filter(
                destination_id=_country_id,
                landing_date__lte=next_12_hours
            )
        except Exception as e:
            return None


    def get_departure_flights(self, _country_id):
        try:
            next_12_hours = timezone.now() + timedelta(hours=12)
            return Flights.objects.filter(
                origin_id=_country_id,
                departure_date__lte=next_12_hours
            )
        except Exception as e:
            return None

    def get_tickets_by_customer(self, _customer_id):
        try:
            return Tickets.objects.filter(customer_id=_customer_id)
        except Exception as e:
            return None