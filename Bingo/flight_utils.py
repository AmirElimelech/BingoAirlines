from .models import Flights, Countries, Tickets, Airline_Companies, Customers, Users, User_Roles, Administrators
from django.utils import timezone

#this function will be used when loggin in , and it returns the airline company according to it's username 
def get_airline_by_username(username):
    try:
        return Airline_Companies.objects.filter(User_Id__Username=username).select_related('User_Id').first()
    except:
        return None



#this function will return users from database in an easier way
def get_customer_by_username(username):
    try:
        return Customers.objects.filter(User_Id__Username=username).select_related('User_Id').first()
    except:
        return None
    


#def this function will return all flights with the specified parameters:
def get_flights_by_parameters(origin_country_id , destination_country_id , date):
    try:
        return Flights.objects.filter(Origin_County_Id=origin_country_id , Destination_Country_Id=destination_country_id , Departure_Time__date=date)
    except:
        return None
    


#this function will return all flights that belongs to specific airline company
def get_flight_by_airline_id(airline_id):
    try:
        return Flights.objects.filter(Airline_company_Id=airline_id)
    except:
        return None
    


# this function returns all landing flights in the next 12 hours in the choosen country
def get_arrival_flights(country_id):
    try:
        return Flights.objects.filter(Destination_Country_Id=country_id , Landing_Time__range=[timezone.now(),timezone.now()+timezone.timedelta(hours=12)])
    except:
        return None




# this function returns all departing flights in the next 12 hours in the choosen country
def get_departure_flights(country_id):
    try:
        return Flights.objects.filter(Origin_County_Id=country_id , Departure_Time__range=[timezone.now(),timezone.now()+timezone.timedelta(hours=12)])
    except:
        return None
    

# #this is the new function to fetch departue flights using amadeus api # i need to make another adjustment to this function which will get token before calling the api 
# import requests
# from datetime import datetime, timedelta

# def get_departure_flights(origin_country_id):
#     try:
#         # Define the API endpoint and parameters for fetching departure flights
#         endpoint = 'https://api.amadeus.com/v2/flights/extensive-search'
#         api_key = '<your_amadeus_api_key>'
#         departure_date = (datetime.now() + timedelta(hours=12)).strftime('%Y-%m-%d')
#         headers = {
#             'Authorization': f'Bearer {api_key}',
#             'Content-Type': 'application/json'
#         }
#         params = {
#             'originCountry': origin_country_id,
#             'departureDate': departure_date
#             # Add more parameters as required by the Amadeus API
#         }

#         # Make the API request
#         response = requests.get(endpoint, headers=headers, params=params)
#         response_data = response.json()

#         # Process the API response and create flight instances
#         flights = []
#         for flight_data in response_data['data']:
#             flight = Flights(
#                 # Extract relevant data from the API response and assign it to the flight instance
#                 # Adjust the mapping based on the structure of the API response and your Flights model
#             )
#             flights.append(flight)

#         return flights

#     except:
#         return None
    



# this function returns all tickets that the customer bought
def get_tickets_by_customer(customer_id):
    try:
        return Tickets.objects.filter(Customer_Id=customer_id)
    except:
        return None
    