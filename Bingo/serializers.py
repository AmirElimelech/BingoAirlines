from rest_framework import serializers
from .models import (
    Flights, Countries, Tickets, Airline_Companies, 
    Customers, Users, User_Roles, Administrators, Airport
)

class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = '__all__'

class AirlineCompaniesSerializer(serializers.ModelSerializer):
    country = CountriesSerializer()

    class Meta:
        model = Airline_Companies
        fields = '__all__'

class FlightsSerializer(serializers.ModelSerializer):
    airline_company = AirlineCompaniesSerializer()
    origin_country = CountriesSerializer()
    destination_country = CountriesSerializer()

    class Meta:
        model = Flights
        fields = '__all__'

class TicketsSerializer(serializers.ModelSerializer):
    flight = FlightsSerializer()

    class Meta:
        model = Tickets
        fields = '__all__'

class UserRolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Roles
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    user_role = UserRolesSerializer()

    class Meta:
        model = Users
        fields = '__all__'

class CustomersSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Customers
        fields = '__all__'

class AdministratorsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Administrators
        fields = '__all__'

class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'
