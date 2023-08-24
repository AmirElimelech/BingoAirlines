from rest_framework import serializers
from Bingo.models import (
    Flights, Countries, Tickets, Airline_Companies, 
    Customers, Users, User_Roles, Administrators, Airport , Booking
)



class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Roles
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    user_role = UserRolesSerializer()
    
    class Meta:
        model = Users
        fields = '__all__'

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class AirlineCompaniesSerializer(serializers.ModelSerializer):
    country = CountriesSerializer(source='country_id')
    user = UsersSerializer(source='user_id')
    
    class Meta:
        model = Airline_Companies
        fields = '__all__'

# class FlightsSerializer(serializers.ModelSerializer):
#     airline_company = AirlineCompaniesSerializer(source='airline_company_id')
#     origin_country = CountriesSerializer(source='origin_country_id')
#     destination_country = CountriesSerializer(source='destination_country_id')
    
#     class Meta:
#         model = Flights
#         fields = '__all__'

# class FlightsSerializer(serializers.ModelSerializer):
#     airline_company = AirlineCompaniesSerializer(source='airline_company_id')
#     origin_country = CountriesSerializer(source='origin_country_id')
#     destination_country = CountriesSerializer(source='destination_country_id')
    
#     class Meta:
#         model = Flights
#         fields = [
#             'id', 'airline_company', 'origin_country', 'destination_country', 
#             'departure_time', 'landing_time', 'remaining_tickets', 'flight_number', 
#             'departure_terminal', 'arrival_terminal'
#         ]



class FlightsSerializer(serializers.ModelSerializer): 
    airline_company = AirlineCompaniesSerializer(source='airline_company_id')
    origin_country = CountriesSerializer(source='origin_country_id')
    destination_country = CountriesSerializer(source='destination_country_id')
    
    class Meta:
        model = Flights
        fields = '__all__'



class FlightsRawSQLSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    departure_time = serializers.DateTimeField()
    landing_time = serializers.DateTimeField()
    remaining_tickets = serializers.IntegerField()
    flight_number = serializers.CharField()
    departure_terminal = serializers.CharField()
    arrival_terminal = serializers.CharField()

    # Fields from related tables
    airline_company_id = serializers.CharField()
    origin_country_id_id = serializers.IntegerField()
    destination_country_id_id = serializers.IntegerField()


       


        



class TicketsSerializer(serializers.ModelSerializer):
    flight = FlightsSerializer(source='flight_id')
    customer = serializers.StringRelatedField(source='customer_id')
    booking = serializers.StringRelatedField()
    
    class Meta:
        model = Tickets
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    user = UsersSerializer(source='user_id')
    
    class Meta:
        model = Customers
        fields = '__all__'

class AdministratorsSerializer(serializers.ModelSerializer):
    user = UsersSerializer(source='user_id')
    
    class Meta:
        model = Administrators
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class ItinerarySerializer(serializers.ModelSerializer):
    customer = serializers.StringRelatedField()
    
    class Meta:
        model = Booking
        fields = '__all__'