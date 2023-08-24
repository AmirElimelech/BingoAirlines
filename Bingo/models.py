# IMPORTS ________________________________________________________________


import re 
import logging
from PIL import Image
from io import BytesIO
from django.db import models
from datetime import timedelta
from django.db import connection
from django.db.models    import Q
from django.utils import  timezone
from django.core import   validators
from Bingo.utils.scheduler import scheduler
from .utils.tasks import download_airline_logo
from django.core.files.base  import  ContentFile
from django.core.validators import MinValueValidator, MaxValueValidator





# Loggers ________________________________________________________________

logger = logging.getLogger(__name__)


# Choices ________________________________________________________________

CURRENCY_CHOICES = [('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('ILS', 'ILS')]
CABIN_CHOICES = [('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First Class')]
TERMINAL_CHOICES = [('1', '1'), ('2', '2'), ('3', '3')]



#Validators ______________________________________________________________

def validate_password_strength(value):
    if len(value) < 6 or not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$", value):
        logging.error("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")
        raise validators.ValidationError("Password should be at least 6 characters, contain an uppercase and lowercase letter, a digit, and a special character.")


def validate_nine_digits(value):
    if len(str(value)) != 9:
        logging.error("ID must be exactly 9 digits long.")
        raise validators.ValidationError("ID must be exactly 9 digits long.")




#Models __________________________________________________________________

# Users model represents individual user accounts
class Users(models.Model):
    id = models.CharField(max_length=9, primary_key=True, validators=[validate_nine_digits])
    username = models.CharField(max_length=255, unique=True, null=False)
    password = models.CharField(max_length=255, null=False , validators=[validate_password_strength])
    email = models.EmailField(max_length=255, unique=True, null=False)
    user_role = models.ForeignKey('User_Roles', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='users/', default='/users/defaultuser.png', null=True)
    is_active = models.BooleanField(default=True)

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
    
    @property
    def is_authenticated(self):
        logging.info(f"Checking if user {self.username} is authenticated.")
        return True
    
    

# User_Roles model represents different user roles ()
class User_Roles(models.Model):
    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=255, unique=True, null=False)

    def __str__(self):
        return self.role_name
    
    class Meta:
        verbose_name_plural = "User Roles"
    


# Customers model represents individual customers
class Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.TextField(null=False)
    last_name = models.TextField(null=False)
    address = models.TextField(null=False , max_length=255)
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
        logging.info(f"Masking credit card number {self.credit_card_no}")
        return '*' * (len(self.credit_card_no) - 4) + self.credit_card_no[-4:]
    








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


# Countries model represents different countries
class Countries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    country_code = models.CharField(max_length=2, unique=True)
    

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Countries"

        

# class Flights(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     airline_company_id = models.ForeignKey('Airline_Companies', to_field='iata_code', on_delete=models.CASCADE)
#     origin_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='origin_flights')
#     destination_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='destination_flights')
#     departure_time = models.DateTimeField(null=False)
#     landing_time = models.DateTimeField(null=False)
#     remaining_tickets = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    
#     def __str__(self):
#         return f'Flight {self.id}'
    
#     class Meta:
#         verbose_name_plural = "Flights"



class Flights(models.Model):
    id = models.BigAutoField(primary_key=True)
    airline_company_id = models.ForeignKey('Airline_Companies', to_field='iata_code', on_delete=models.CASCADE)
    origin_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='origin_flights')
    destination_country_id = models.ForeignKey('Countries', on_delete=models.CASCADE, related_name='destination_flights')
    departure_time = models.DateTimeField(null=False)
    landing_time = models.DateTimeField(null=False)
    remaining_tickets = models.IntegerField(null=False, validators=[MinValueValidator(0)])
    flight_number = models.CharField(max_length=10)  
    departure_terminal = models.CharField(max_length=1, choices=TERMINAL_CHOICES, null=True, blank=True)
    arrival_terminal = models.CharField(max_length=1, choices=TERMINAL_CHOICES, null=True, blank=True)

    def __str__(self):
        return f'Flight {self.id}'
    
    class Meta:
        verbose_name_plural = "Flights"


# class Itinerary(models.Model):
#     customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     booking_date = models.DateTimeField(auto_now_add=True)  # The date when the customer made the booking.
#     total_price = models.DecimalField(max_digits=9, decimal_places=2)  # Total price for the whole booking.

#     # Journey details
#     currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, default='USD')
#     cabin = models.CharField(max_length=10, choices=CABIN_CHOICES, default='ECONOMY')
#     adult_traveler_count = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], default=1)
#     child_traveler_count = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)], default=0)

#     # Any other relevant fields that pertain to the overall journey.

#     def __str__(self):
#         return f'Itinerary {self.id} for Customer {self.customer_id}'

#     class Meta:
#         verbose_name_plural = "Itineraries"



class Booking(models.Model):
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=9, decimal_places=2)
    
    def __str__(self):
        return f'Booking {self.id} for Customer {self.customer_id}'
    
    class Meta:
        verbose_name_plural = "Bookings"






    
        


# # Tickets model represents individual flight tickets
# class Tickets(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
#     customer_id = models.ForeignKey('Customers', on_delete=models.CASCADE)

#     def __str__(self):
#         return f'Ticket {self.id}'
    
#     class Meta:
#         verbose_name_plural = "Tickets"


class Tickets(models.Model):
    id = models.BigAutoField(primary_key=True)
    flight_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
    customer_id = models.ForeignKey('Customers', on_delete=models.CASCADE)
    Booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    
    # Segment-specific details
    currency = models.CharField(max_length=4, choices=CURRENCY_CHOICES, default='USD')
    cabin = models.CharField(max_length=10, choices=CABIN_CHOICES, default='ECONOMY')
    adult_traveler_count = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)], default=1)
    child_traveler_count = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9)], default=0)
    
    def __str__(self):
        return f'Ticket {self.id}'
    
    class Meta:
        verbose_name_plural = "Tickets"
    


    


class Airport(models.Model):
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=3 , primary_key=True)

    def __str__(self):
        return self.name
    



class Airline_Companies(models.Model):
    iata_code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, unique=True)
    logo = models.ImageField(upload_to='airline_logos/', null=True, blank=True)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Airline Companies"




    # def save(self, *args, **kwargs): 
    #     # logo save logic
    #     if self.logo and self.logo.name != f'airline_logos/{self.iata_code}.png':


            
    #         pil_image = Image.open(self.logo)
    #         pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)
    #         buffer = BytesIO()
    #         pil_image.save(buffer, format='PNG')
    #         filename = f'{self.iata_code}.png'
    #         self.logo.save(filename, ContentFile(buffer.getvalue()), save=False)
            
    #     # If no logo is provided and the IATA code is given, schedule a download task
    #     elif self.iata_code and not self.logo:
    #         logger.info(f"Logo not provided for {self.iata_code}. Scheduling download task...")
    #         start_time = datetime.now() + timedelta(seconds=5)
    #         scheduler.add_job(download_airline_logo, 'date', run_date=start_time, args=[self.iata_code])
            
    #     super(Airline_Companies, self).save(*args, **kwargs)

    def save(self, *args, **kwargs): 
        try:
            # logo save logic
            if self.logo and self.logo.name != f'airline_logos/{self.iata_code}.png':
                pil_image = Image.open(self.logo)
                pil_image = pil_image.resize((100, 100), Image.ANTIALIAS)
                buffer = BytesIO()
                pil_image.save(buffer, format='PNG')
                filename = f'{self.iata_code}.png'
                self.logo.save(filename, ContentFile(buffer.getvalue()), save=False)
            
            # First, save the Airline_Companies record to the database
            super(Airline_Companies, self).save(*args, **kwargs)

            # After saving, if no logo is provided and the IATA code is given, schedule a download task
            if self.iata_code and not self.logo:
                logger.info(f"Logo not provided for {self.iata_code}. Scheduling download task...")
                scheduler.add_job(download_airline_logo, args=[self.iata_code])

        except Exception as e:
            logger.error(f"An error occurred while saving the Airline_Companies model: {e}")

    
    

            








# Data Access Layer ______________________________________________________
class DAL:


# CRUD methods
    
    def get_by_id(self, model, value, field_name=None):
        try:
            # If field_name isn't provided, default to the primary key field
            if not field_name:
                field_name = model._meta.pk.name

            # Create a dictionary to hold the query parameters
            query = {field_name: value}

            return model.objects.get(**query)
        except model.DoesNotExist:
            logger.error(f"Error fetching instance of {model.__name__} with {field_name}={value}")
            return None



    def get_all(self, model):
        try:
            return model.objects.all()
        except Exception as e:
            logger.error(f"Error fetching all instances of {model.__name__}. Error: {str(e)}")
            return None



    def add(self, model, **kwargs):
        try:
            instance = model.objects.create(**kwargs)
            if instance:
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
            logger.error(f"Error updating instance {instance}. Error: {str(e)}")
            return None

    def add_all(self, model, list_of_dicts):
        try:
            return model.objects.bulk_create([model(**kwargs) for kwargs in list_of_dicts])
        except Exception as e:
            logger.error(f"Error bulk creating {model.__name__} instances with kwargs: {list_of_dicts}. Error: {str(e)}")
            return None

    def remove(self, instance):
        try:
            instance.delete()
            logger.info(f"Successfully deleted instance {instance}")
            return True
        except Exception as e:
            logger.error(f"Error deleting instance {instance}. Error: {str(e)}")
            return None

# Custom methods _________________________________________________________



    def filter_by_query(self, model, query=None):
        """
        Filter a model based on provided query arguments used by AutoComplete method in views.flight_views.py
        """
        try:
            if query:
                return model.objects.filter(query)
            else:
                return model.objects.all()
        except Exception as e:
            logger.error(f"Error fetching instances of {model.__name__} based on query. Error: {str(e)}")
            return None
    

    def get_airlines_by_country(self, country_id):

        """
        Get all airlines for a given country ID
        """
        try:
            return Airline_Companies.objects.filter(country_id=country_id)
        except Exception as e:
            logger.error(f"Error fetching airlines for country ID {country_id}. Error: {str(e)}")
            return None
        


    def get_flights_by_origin_country_id(self, country_id):

        """
        Get all flights with a given origin country ID
        """

        try:
            return Flights.objects.filter(origin_country_id=country_id)
        except Exception as e:
            logger.error(f"Error fetching flights with origin country ID {country_id}. Error: {str(e)}")
            return None



    def get_flights_by_destination_country_id(self, country_id):

        """
        Get all flights with a given destination country ID
        """

        try:
            return Flights.objects.filter(destination_country_id=country_id)
        except Exception as e:
            logger.error(f"Error fetching flights with destination country ID {country_id}. Error: {str(e)}")
            return None



    def get_flights_by_departure_date(self, date):

        """
        Get all flights with a given departure date
        """

        try:
            return Flights.objects.filter(departure_time=date)
        except Exception as e:
            logger.error(f"Error fetching flights with departure date {date}. Error: {str(e)}")
            return None



    def get_flights_by_landing_date(self, date):

        """
        Get all flights with a given landing date
        """

        try:
            return Flights.objects.filter(landing_time=date)
        except Exception as e:
            logger.error(f"Error fetching flights with landing date {date}. Error: {str(e)}")
            return None



    # def get_flights_by_customer(self, customer_id):

    #     """
    #     Get all flights for a given customer ID
    #     """

    #     try:
    #         return Flights.objects.filter(customer_id=customer_id)
    #     except Exception as e:
    #         logger.error(f"Error fetching flights for customer ID {customer_id}. Error: {str(e)}")
    #         return None
        


    def get_flights_by_customer(self, customer_id):
        """
        Get all flights for a given customer ID
        """
        try:
            # Fetch all itineraries for the customer
            bookings = Booking.objects.filter(customer_id=customer_id)

            # Fetch all tickets that are part of these itineraries
            tickets = Tickets.objects.filter(booking__in=bookings)

            # Extract flight IDs from the tickets
            flight_ids = [ticket.flight_id.id for ticket in tickets]

            # Fetch all flights using the extracted flight IDs
            flights = Flights.objects.filter(id__in=flight_ids)

            return flights
        except Exception as e:
            logger.error(f"Error fetching flights for customer ID {customer_id}. Error: {str(e)}")
            return None




    def get_airline_by_username(self, username):

        """
        Get an airline company by its username
        """

        try:
            return Airline_Companies.objects.get(user__username=username)
        except Airline_Companies.DoesNotExist:
            logger.error(f"Airline company not found with username {username}")
            return None



    def get_customer_by_username(self, username):

        """
        Get a customer by its username
        """

        try:
            return Customers.objects.get(user__username=username)
        except Customers.DoesNotExist:
            logger.error(f"Customer not found with username {username}")
            return None



    def get_user_by_username(self, username):

        """
        Get a user by its username
        """

        try:
            return Users.objects.get(username=username)
        except Users.DoesNotExist:
            logger.error(f"User not found with username {username}")
            return None

    # #v1
    # # this function is uselles since i'm goin to be using my own search flight function based on Amadeus API

    # def get_flights_by_parameters(self, origin_country_id, destination_country_id, date):

    #     """
    #     Get all flights with a given origin country ID, destination country ID, and departure date
    #     """

    #     try:
    #         return Flights.objects.filter(
    #             origin_country_id=origin_country_id,
    #             destination_country_id=destination_country_id,
    #             departure_time=date
    #         )
    #     except Exception as e:
    #         logger.error(f"Error fetching flights with origin country ID {origin_country_id}, destination country ID {destination_country_id}, and departure date {date}. Error: {str(e)}")
    #         return None



    #V2

    # def get_flights_by_parameters(self, parameters):
    #     # Extracting parameters
    #     origin_country_id = parameters.get('origin_country_id')
    #     destination_country_id = parameters.get('destination_country_id')
    #     departure_date = parameters.get('departure_date')
    #     return_date = parameters.get('return_date', None)
        
    #     # Building the query for departure flights
    #     departure_query = Q(
    #         origin_country_id=origin_country_id, 
    #         destination_country_id=destination_country_id,
    #         departure_time__date=departure_date
    #     )
        
    #     if return_date:
    #         # Building the query for return flights
    #         return_query = Q(
    #             origin_country_id=destination_country_id, 
    #             destination_country_id=origin_country_id,
    #             departure_time__date=return_date
    #         )
    #         # Combining both departure and return flight queries
    #         combined_query = departure_query | return_query
    #     else:
    #         combined_query = departure_query
        
    #     # Querying the database
    #     flights = Flights.objects.filter(combined_query).values(
    #         'origin_country_id',
    #         'destination_country_id',
    #         'departure_time',
    #         'landing_time'
    #     )
        
    #     return flights




    def get_flights_by_parameters(self, parameters):
        # Extracting parameters
        origin_country_id = parameters.get('origin_country_id')
        destination_country_id = parameters.get('destination_country_id')
        departure_date = parameters.get('departure_date')
        return_date = parameters.get('return_date', None)
        
        # Logging the received parameters
        logging.info(f"Received Parameters: Origin Country ID: {origin_country_id}, Destination Country ID: {destination_country_id}, Departure Date: {departure_date}, Return Date: {return_date}")
        

        departure_query = Q(
            origin_country_id_id=origin_country_id, 
            destination_country_id_id=destination_country_id,
            departure_time__contains=departure_date
        )
        
        if return_date:
            # Building the query for return flights
            return_query = Q(
                origin_country_id_id=destination_country_id, 
                destination_country_id_id=origin_country_id,
                departure_time__contains=departure_date

            )
            # Combining both departure and return flight queries
            combined_query = departure_query | return_query
        else:
            combined_query = departure_query
        
        # Preparing the query (not executing it yet)
        flights_query = Flights.objects.filter(combined_query)
        
        # Printing the SQL query
        print(str(flights_query.query))
        
        flights = flights_query.values(
            'id',
            'origin_country_id_id',
            'destination_country_id_id',
            'departure_time',
            'landing_time',
            'remaining_tickets',
            'flight_number',  
            'airline_company_id',
            'arrival_terminal',
            'departure_terminal'
        )

        print(flights)
        
        # Logging the results
        logging.info(f"Number of flights found: {len(flights)}")
        
        return flights


    

    

    # def get_flights_by_parameters(self, parameters):
    #     # Extracting parameters
    #     origin_country_id = parameters.get('origin_country_id')
    #     destination_country_id = parameters.get('destination_country_id')
    #     departure_date = parameters.get('departure_date')
    #     return_date = parameters.get('return_date', None)
        
    #     # Logging the received parameters
    #     logging.info(f"Received Parameters: Origin Country ID: {origin_country_id}, Destination Country ID: {destination_country_id}, Departure Date: {departure_date}, Return Date: {return_date}")
        
    #     # Constructing raw SQL query
    #     query = f"""
    #     SELECT * 
    #     FROM bingo_air_db.bingo_flights 
    #     WHERE origin_country_id_id = {origin_country_id}
    #     AND destination_country_id_id = {destination_country_id}
    #     AND DATE(departure_time) = '{departure_date}'
    #     """
        
    #     flights = []
    #     with connection.cursor() as cursor:
    #         cursor.execute(query)
    #         columns = [col[0] for col in cursor.description]
    #         for row in cursor.fetchall():
    #             flights.append(dict(zip(columns, row)))

    #     # Logging the results
    #     logging.info(f"Number of flights found: {len(flights)}")
        
    #     return flights









    def get_flights_by_airline_id(self, airline_id):

        """
        Get all flights for a given airline ID
        """

        try:
            return Flights.objects.filter(airline_company_id=airline_id)
        except Exception as e:
            logger.error(f"Error fetching flights for airline ID {airline_id}. Error: {str(e)}")
            return None



    def get_arrival_flights(self, country_id):

        """
        Get all arrival flights in the next 12 hours for a given country ID
        """

        try:
            next_12_hours = timezone.now() + timedelta(hours=12)
            return Flights.objects.filter(
                destination_country_id=country_id,
                landing_time__lte=next_12_hours
            )
        except Exception as e:
            logger.error(f"Error fetching arrival flights for country ID {country_id} within the next 12 hours. Error: {str(e)}")
            return None



    def get_departure_flights(self, country_id):

        """
        Get all departure flights in the next 12 hours for a given country ID
        """

        try:
            next_12_hours = timezone.now() + timedelta(hours=12)
            return Flights.objects.filter(
                origin_country_id=country_id,
                departure_time__lte=next_12_hours
            )
        except Exception as e:
            logger.error(f"Error fetching departure flights for country ID {country_id} within the next 12 hours. Error: {str(e)}")
            return None



    def get_tickets_by_customer(self, customer_id):

        """
        Get all tickets for a given customer ID
        """

        try:
            return Tickets.objects.filter(customer_id=customer_id)
        except Exception as e:
            logger.error(f"Error fetching tickets for customer ID {customer_id}. Error: {str(e)}")
            return None

        


