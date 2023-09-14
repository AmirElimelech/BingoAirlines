
import logging 
from django.db.models import Q
from rest_framework import status
from django.http import JsonResponse
from Bingo.decorators import login_required
from django.middleware.csrf import get_token
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from Bingo.facades.facade_base import FacadeBase
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as django_logout
from Bingo.facades.anonymous_facade import AnonymousFacade
from Bingo.models import (Airport , DAL , User_Roles , Users , Customers 
                     , Airline_Companies , Administrators , validate_nine_digits )  
from ..serializers import    (FlightsSerializer, AirlineCompaniesSerializer, CountriesSerializer , 
                                                           FlightsRawSQLSerializer , AirportSerializer )




logger = logging.getLogger(__name__)



####################################### User Views #########################################

@api_view(['POST'])
def user_registration_api(request):
    logger.info("Processing user registration request")

    # Extracting data from the request
    user_data = {
        'id': request.POST.get('user[id]', None),
        'username': request.POST.get('user[username]', None),
        'password': request.POST.get('user[password]', None),
        'email': request.POST.get('user[email]', None),
        'user_role': request.POST.get('user[user_role]', None),
        'is_active': request.POST.get('user[is_active]', True)
    }
    logger.debug(f"Received user data: {user_data}")

    customer_data = {
        'first_name': request.POST.get('customer[first_name]', None),
        'last_name': request.POST.get('customer[last_name]', None),
        'address': request.POST.get('customer[address]', None),
        'phone_no': request.POST.get('customer[phone_no]', None),
        'credit_card_no': request.POST.get('customer[credit_card_no]', None)
    }

    user_role_id = user_data.get('user_role', None)
    logger.debug(f"Extracted user_role_id: {user_role_id}")

    try:
        existing_user = Users.objects.filter(id=user_data['id']).first()
        if existing_user:
            return Response({"error": "User with provided ID already exists."}, status=400)

        user_role_instance = User_Roles.objects.get(id=user_role_id)
        
        # Adding image upload to user instance creation
        user_instance = Users(
            id=user_data['id'],
            username=user_data['username'],
            password=make_password(user_data['password']),
            email=user_data['email'],
            user_role=user_role_instance,
            is_active=user_data.get('is_active', True),
            image=request.FILES.get('user[image]', None)
        )
        user_instance.save()
        logger.debug(f"Successfully saved User instance: {user_instance}")

        # Check if a customer with the provided phone_no or user_id already exists
        existing_customer_by_phone = Customers.objects.filter(phone_no=customer_data['phone_no']).first()
        existing_customer_by_user_id = Customers.objects.filter(user_id=user_instance.id).first()

        if existing_customer_by_phone:
            return Response({"error": "Customer with provided phone number already exists."}, status=400)

        if existing_customer_by_user_id:
            return Response({"error": "Customer with provided user ID already exists."}, status=400)

        # Link the user instance to the customer data and save customer
        customer_data['user_id'] = user_instance.id

        anonymous_facade = AnonymousFacade(request)
        customer_instance = anonymous_facade.add_customer(customer_data)
        logger.info(f"Successfully created Customer instance: {customer_instance}")

        return Response({"message": "Registration successful."}, status=201)

    except User_Roles.DoesNotExist:
        return Response({"error": "Invalid user_role ID provided."}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return Response({"error": "An unexpected error occurred."}, status=500)





@api_view(["GET"])
def initialize_session(request):
    """
    Endpoint to initialize the session after login.
    """
    return JsonResponse({"detail": "Session initialized", "status": "success"}, status=200)





@api_view(["POST"])
def login_view_api(request):
    """Login view for the BingoAirlines project."""

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        csrf_token = get_token(request)
        logging.debug(f"login_view_api - CSRF Token sent to client: {csrf_token}")

        username = request.POST['username']
        password = request.POST['password']
        facade = AnonymousFacade(request)
        
        login_token = facade.login(username, password)
        user_role = Users.objects.get(id=login_token.user_id).user_role.role_name

        response_data = {
            "detail": "Login successful", 
            "status": "success",
            "username": username,
            "id": str(login_token.user_id),
            "user_role": user_role
        }

        if login_token.user_role == "Customer":
            user_instance = Users.objects.get(username=username)
            customer = Customers.objects.get(user_id=user_instance)
            response_data.update({
                "customer_id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "address": customer.address,
                "phone_no": customer.phone_no,
                "credit_card_no": customer.credit_card_no
            })

        elif login_token.user_role == "Airline Company":
            user_instance = Users.objects.get(username=username)
            airline = Airline_Companies.objects.get(user_id=user_instance)
            

        elif login_token.user_role == "Administrator":
            user_instance = Users.objects.get(username=username)
            administrator = Administrators.objects.get(user_id=user_instance)
           

        # Set session data after database operations
        request.session['login_token'] = {'user_id': login_token.user_id, 'user_role': login_token.user_role}
        logging.info(f"login_view_api - Setting login token in session: {request.session['login_token']}")
        logging.info(f"login_view_api - Welcome {username}! Successfully logged in as {login_token.user_role}.")

        return JsonResponse(response_data, status=200)

    except ValidationError as e:
        error_message = str(e)
        logger.error(f"Login error: {error_message}")
        return JsonResponse({"error": error_message}, status=400)
    except Exception as e:
        error_message = "An unexpected error occurred during login."
        logger.error(f"Unexpected login error: {str(e)}")
        return JsonResponse({"error": error_message}, status=500)




@login_required
@api_view(['GET'])
def logout_view_api(request): 
    """
    Logout API for the BingoAirlines project.
    """
    try:
        if 'login_token' in request.session:
            # Log the username before invalidating the session
            # Invalidate the session and log the user out
            del request.session['login_token']
            django_logout(request)

            logging.info(f"logout_api - Successfully logged out")

            # Check if there's a user in the session after logout
            login_token = request.session.get('login_token')
            if login_token:
                logging.warning(f"logout_api - User still in session after logout: {login_token.get('user_id')}")
            else:
                logging.info(f"logout_api - No user in session after logout. user set to {request.user}")

            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"logout_api - Error during logout: {str(e)}")
        return Response({"error": "Logout failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)






@api_view(['GET'])
def get_user_image_url_api(request, user_id):
    """
    Get the user's image URL so it can be shown in the UI for the logged in user.
    """
    
    # Extracting login token from the session
    login_token = request.session.get('login_token', None)
    logger.info(f"get_user_image_url_api - Login token from session: {login_token}")

    try:
        dal = DAL()

        # If the length of the user_id is not 9 digits, treat it as a customer ID
        if len(user_id) != 9:
            try:
                customer = dal.get_by_id(Customers, user_id)
                if not customer:
                    logger.warning(f"get_user_image_url_api - No customer found with ID: {user_id}")
                    return Response({"error": "Customer not found."}, status=404)
                
                user_id = customer.user_id.id
            except Exception as e:
                logger.error(f"get_user_image_url_api - An error occurred while trying to fetch user ID for customer ID: {user_id}. Error: {str(e)}")
                return Response({"error": "Internal server error while fetching user ID from customer."}, status=500)
        
        # Use validate_nine_digits to validate user_id
        try:
            validate_nine_digits(user_id)
        except ValidationError:
            logger.warning(f"get_user_image_url_api - Invalid user ID format received: {user_id}")
            return Response({"error": "Invalid user ID format. Ensure it's 9 digits long."}, status=400)
        
        user = dal.get_by_id(Users, user_id)
        
        if user:
            logger.info(f"get_user_image_url_api - Successfully fetched image URL for user ID: {user_id}")
            return Response({"image_url": user.image_url}, status=200)
        else:
            logger.warning(f"get_user_image_url_api - No user found with ID: {user_id}")
            return Response({"error": "User not found."}, status=404)
            
    except Exception as e:
        logger.error(f"get_user_image_url_api - An error occurred while trying to fetch image URL for user ID: {user_id}. Error: {str(e)}")
        return Response({"error": "Internal server error."}, status=500)




####################################### Generic Views #########################################

@csrf_exempt
@api_view(['GET'])
def autocomplete_api(request):   

    """
    Get a list of airports matching the query string , used as a helper to search for airports in the UI

    """


    q = request.GET.get('q', '')
    
    # Create the DAL instance and filter the airports
    dal_instance = DAL()
    query_params = Q(name__icontains=q) | Q(iata_code__icontains=q)
    airports = dal_instance.filter_by_query(Airport, query=query_params)

    results = [airport.name for airport in airports] if airports else []
    logging.info(f"Found {len(results)} airports matching query: {q}")
    return JsonResponse(results, safe=False)



@csrf_exempt
@api_view(['GET'])
def get_airport_by_iata_code_api(request, iata_code):

    """
    Get an airport from the database by its IATA code
    """

    try:
        
        facade = FacadeBase(request)
        airport = facade.get_airport_by_iata_code(iata_code)
        if airport:
            serializer = AirportSerializer(airport)  # Assuming you have an AirportSerializer
            logger.info(f"Successfully fetched airport with IATA code: {iata_code}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Airport with IATA code {iata_code} not found.")
        return Response({"error": "Airport not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching airport with IATA code {iata_code}: {str(e)}")
        return Response({"error": "An error occurred while fetching the airport."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







@csrf_exempt
@api_view(['GET'])
def get_all_flights_api(request):

    """
    Get all flights from the database without pagination
    """

    try:
        facade = FacadeBase(request)
        flights = facade.get_all_flights()

        serializer = FlightsSerializer(flights, many=True)

        logger.info("Successfully fetched all flights.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching all flights: {str(e)}")
        return Response({"error": "Error fetching flights."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@csrf_exempt
@api_view(['GET'])
def get_flight_by_id_api(request, flight_number):

    """
    Get a flight from the database by its Flight number 
    """

    try:
        
        facade = FacadeBase(request)
        flight = facade.get_flight_by_id(flight_number) 
        if flight:
            serializer = FlightsSerializer(flight)
            logger.info(f"Successfully fetched flight with flight_number: {flight_number}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Flight with flight_number {flight_number} not found.")
        return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching flight with flight_number {flight_number}: {str(e)}")
        return Response({"error": "An error occurred while fetching the flight."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@csrf_exempt
@api_view(['GET'])
def get_all_airlines_api(request):

    """
    Get all airlines from the database without pagination
    """

    try:
        facade = FacadeBase(request)
        airlines = facade.get_all_airlines()

        serializer = AirlineCompaniesSerializer(airlines, many=True)

        logger.info("Successfully fetched all airlines.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching all airlines: {str(e)}")
        return Response({"error": "Error fetching airlines."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@csrf_exempt
@api_view(['GET'])
def get_airline_by_id_api(request, iata_code):

    """
    Get an airline from the database by its IATA code
    """

    try:
        facade = FacadeBase(request)
        airline = facade.get_airline_by_id(iata_code)
        
        if airline:
            serializer = AirlineCompaniesSerializer(airline)
            logger.info(f"Successfully fetched airline with IATA code: {iata_code}")
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"Airline with IATA code {iata_code} not found.")
        return Response({"error": "Airline not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching airline with IATA code {iata_code}: {str(e)}")
        return Response({"error": "An error occurred while fetching the airline."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
def get_flights_by_parameters_api(request):
    """
    Get flights from the database based on search criteria
    """
    try:
        # Extract parameters from the request body
        data = request.data
        
        facade = FacadeBase(request)
        flights = facade.get_flights_by_parameters(data)
        
        if flights:
            serializer = FlightsRawSQLSerializer(flights, many=True)

            logger.info(f"Successfully fetched flights based on search criteria.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        logger.warning(f"No flights found based on search criteria.")
        return Response({"message": "No flights found.", "data": []}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error fetching flights based on search criteria: {str(e)}")
        return Response({"error": "An error occurred while fetching the flights."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@csrf_exempt
@api_view(['GET'])
def get_all_countries_api(request):

    """
    Get all countries from the database without pagination
    """

    try:
        facade = FacadeBase(request)
        countries = facade.get_all_countries()

        # Serialize the countries directly without pagination
        serializer = CountriesSerializer(countries, many=True)

        logger.info("Successfully fetched all countries.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching all countries: {str(e)}")
        return Response({"error": "Error fetching countries."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@csrf_exempt
@api_view(['GET'])
def get_country_by_id_api(request, country_code):

    """
    Get a country from the database by its country code
    """
    
    try:
        # Validate that the country code is in the expected format
        if not (len(country_code) == 2 and country_code.isalpha()):
            return Response({"error": "Invalid country code format. It should be a 2-character alphabetic code."}, status=status.HTTP_400_BAD_REQUEST)

        facade = FacadeBase(request)
        country = facade.get_country_by_id(country_code)
        if country:
            serializer = CountriesSerializer(country)
            logger.info(f"Successfully fetched country with code: {country_code}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Country with code {country_code} not found.")
        return Response({"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        logger.error(f"Error fetching country with code {country_code}: {str(e)}")
        return Response({"error": "An error occurred while fetching the country."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@csrf_exempt
@api_view(['GET'])
def get_all_airports_api(request):
    """
    Get all airports from the database without pagination
    """

    try:
        facade = FacadeBase(request)
        airports = facade.get_all_airports()

        serializer = AirportSerializer(airports, many=True)

        logger.info("Successfully fetched all airports.")
        return Response(serializer.data)
    except Exception as e:
        logger.error(f"Error fetching all airports: {str(e)}")
        return Response({"error": "Error fetching airports."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
