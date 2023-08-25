

import logging
from rest_framework import status
from Api.permissions import IsAdministrator
from rest_framework.response import   Response
from rest_framework.decorators   import  api_view
from Bingo.utils.login_token     import    LoginToken
from Bingo.decorators import check_permissions , login_required
from Bingo.facades.administrator_facade import      AdministratorFacade
from ..serializers import AirlineCompaniesSerializer, CustomersSerializer, AdministratorsSerializer




logger = logging.getLogger(__name__)



def get_login_token_from_request(request):

    """
    Extract the login token from the session data of the request.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - LoginToken object if the token exists in the session, otherwise None.
    """

    login_token_dict = request.session.get('login_token')
    if login_token_dict:
        return LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
    return None




@login_required
@api_view(['GET'])
@check_permissions(IsAdministrator)
def get_all_customers_api(request):

    """
    Get all customers from the database.
    """
    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        customers = facade.get_all_customers()
        
        serializer = CustomersSerializer(customers, many=True)
        if not customers:
            logger.info("No customers found in the database.")
            return Response({"message": "No customers found in the database."}, status=status.HTTP_200_OK)
        
        logger.info("Successfully fetched all customers.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return Response({"error": "Error fetching customers."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





@login_required
@api_view(['POST'])
@check_permissions(IsAdministrator)
def add_airline_api(request):

    """
    Add a new airline to the database.
    """

    try:
        # Get a mutable copy of the data dict from the request object.
        # The original request.data object is immutable (cannot be changed once created !)
        data = request.data.copy()

        # If the 'country_id' key exists in the data, convert its value to an integer.
        # This ensures that the 'country_id' is in the correct data type before further processing.
        if 'country_id' in data:
            data['country_id'] = int(data['country_id'])

        # Similar to the previous step, but for 'user_id'.
        if 'user_id' in data:
            data['user_id'] = int(data['user_id'])

        # Create an instance of the AdministratorFacade class, which likely contains business logic 
        # or interacts with the database to perform operations related to administrators.
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        
        # Call the 'add_airline' method from the facade with the provided data to create a new airline.
        # The result is likely an instance of the created airline.
        airline = facade.add_airline(request.data)
        
        # Serialize the airline instance into a format suitable for sending in a response.
        serializer = AirlineCompaniesSerializer(airline)


        logger.info("Successfully added airline.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding airline: {str(e)}")
        return Response({"error": "Error adding airline."}, status=status.HTTP_400_BAD_REQUEST)





@login_required
@api_view(['POST'])
@check_permissions(IsAdministrator)
def add_customer_api(request):

    """
    Add a new customer to the database.
    """

    try:
        # Initialize the AdministratorFacade with the current request, user, and login token
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        
        # Use the facade to add a new customer using the provided request data
        customer = facade.add_customer(request.data)
        serializer = CustomersSerializer(customer)
        logger.info("Successfully added customer.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding customer: {str(e)}")
        return Response({"error": "Error adding customer."}, status=status.HTTP_400_BAD_REQUEST)





@login_required
@api_view(['POST'])
@check_permissions(IsAdministrator)
def add_administrator_api(request):

    """
    Add a new administrator to the database.
    """

    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        admin = facade.add_administrator(request.data)
        serializer = AdministratorsSerializer(admin)
        logger.info("Successfully added administrator.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding administrator: {str(e)}")
        return Response({"error": "Error adding administrator."}, status=status.HTTP_400_BAD_REQUEST)





@login_required
@api_view(['DELETE'])
@check_permissions(IsAdministrator)
def remove_airline_api(request, iata_code):

    """
    Remove an airline from the database.
    """

    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        facade.remove_airline({"iata_code": iata_code})
        logger.info(f"Successfully removed airline with IATA code: {iata_code}.")
        return Response({"message": "Airline successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing airline: {str(e)}")
        return Response({"error": "Error removing airline."}, status=status.HTTP_400_BAD_REQUEST)





@login_required
@api_view(['DELETE'])
@check_permissions(IsAdministrator)
def remove_customer_api(request, customer_id):

    """
    Remove a customer from the database.
    """

    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        facade.remove_customer({"id": customer_id})
        logger.info(f"Successfully removed customer with ID: {customer_id}.")
        return Response({"message": "Customer successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing customer: {str(e)}")
        return Response({"error": "Error removing customer."}, status=status.HTTP_400_BAD_REQUEST)







@login_required
@api_view(['DELETE'])
@check_permissions(IsAdministrator)
def remove_administrator_api(request, admin_id):

    """
    Remove an administrator from the database.
    """
    
    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        facade.remove_administrator({"id": admin_id})
        logger.info(f"Successfully removed administrator with ID: {admin_id}.")
        return Response({"message": "Administrator successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing administrator: {str(e)}")
        return Response({"error": "Error removing administrator."}, status=status.HTTP_400_BAD_REQUEST)

