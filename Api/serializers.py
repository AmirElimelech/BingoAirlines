
from rest_framework import serializers
from Bingo.models import (
    Flights, Countries, Tickets, Airline_Companies, 
    Customers, Users, User_Roles, Administrators, Airport , Booking 
)


class UsersSerializer(serializers.ModelSerializer):
    user_role = serializers.PrimaryKeyRelatedField(queryset=User_Roles.objects.all())
    
    class Meta:
        model = Users
        fields = '__all__'

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Roles
        fields = '__all__'



class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class AirlineCompaniesSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(source='country_id')    
    class Meta:
        model = Airline_Companies
        fields = '__all__'



class CustomersSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user_id.email')
    
    class Meta:
        model = Customers
        fields = ('id', 'first_name', 'last_name', 'address', 'phone_no', 'credit_card_no', 'user_id', 'email')



class AdministratorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Administrators
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class FlightsSerializer(serializers.ModelSerializer): 
    airline_company = AirlineCompaniesSerializer(source='airline_company_id')
    origin_airport = AirportSerializer()
    destination_airport = AirportSerializer()

    
    class Meta:
        model = Flights
        fields = '__all__'



class FlightsRawSQLSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    flight_number = serializers.CharField()
    departure_time = serializers.DateTimeField()
    landing_time = serializers.DateTimeField()
    remaining_tickets = serializers.IntegerField()
    departure_terminal = serializers.CharField()
    arrival_terminal = serializers.CharField()
    
    # Fields from related tables
    airline_company_id = serializers.CharField()
    origin_airport__iata_code = serializers.CharField()
    destination_airport__iata_code = serializers.CharField()


class BookingSerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    
    class Meta:
        model = Booking
        fields = '__all__'

class TicketsSerializer(serializers.ModelSerializer):
    flight = FlightsSerializer(source='flight_number_ref')
    customer = serializers.StringRelatedField(source='customer_id')
    booking = serializers.StringRelatedField()
    
    class Meta:
        model = Tickets
        fields = '__all__'



class OriginDestinationAirportSerializer(serializers.Serializer):
    iata_code = serializers.CharField()
    country_code = serializers.CharField()


class AirlineDetailSerializer(serializers.Serializer):
    name = serializers.CharField()
    iata_code = serializers.CharField()


class BookingDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()  
    booking_date = serializers.DateTimeField()
    total_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    flight_number = serializers.CharField()
    origin_airport = OriginDestinationAirportSerializer()
    destination_airport = OriginDestinationAirportSerializer()
    departure_time = serializers.DateTimeField()
    landing_time = serializers.DateTimeField()
    departure_terminal = serializers.CharField()
    arrival_terminal = serializers.CharField()
    airline = AirlineDetailSerializer()
    cabin = serializers.CharField()
    adult_traveler_count = serializers.IntegerField()
    child_traveler_count = serializers.IntegerField()
    currency = serializers.CharField()







class AirportBookingSerializer(serializers.Serializer):
    iataCode = serializers.CharField(max_length=3)

class AirlineBookingSerializer(serializers.Serializer):
    iataCode = serializers.CharField(max_length=2)

class BookingCreateSerializer(serializers.Serializer):
    booking_date = serializers.DateTimeField()
    total_price = serializers.DecimalField(max_digits=9, decimal_places=2)
    flight_number = serializers.CharField(max_length=10)
    origin_airport = AirportBookingSerializer()
    destination_airport = AirportBookingSerializer()
    departure_time = serializers.DateTimeField()
    landing_time = serializers.DateTimeField()
    departure_terminal = serializers.CharField(max_length=5, required=False)
    arrival_terminal = serializers.CharField(max_length=5, required=False)
    airline = AirlineBookingSerializer()
    cabin = serializers.CharField(max_length=20)
    adult_traveler_count = serializers.IntegerField()
    child_traveler_count = serializers.IntegerField()
    currency = serializers.CharField(max_length=5)
    remaining_tickets = serializers.IntegerField()

   











