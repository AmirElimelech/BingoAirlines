
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import AirlineCompaniesSerializer, CustomersSerializer, AdministratorsSerializer
from Bingo.facades.administrator_facade import AdministratorFacade
from Bingo.decorators import check_permissions , login_required
from Api.permissions import IsAdministrator
from Bingo.utils.login_token import LoginToken
import logging

logger = logging.getLogger(__name__)

def get_login_token_from_request(request):
    login_token_dict = request.session.get('login_token')
    if login_token_dict:
        return LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
    return None

@login_required
@api_view(['GET'])
@check_permissions(IsAdministrator)
def get_all_customers_api(request):
    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        customers = facade.get_all_customers()
        serializer = CustomersSerializer(customers, many=True)
        logger.info("Successfully fetched all customers.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        return Response({"error": "Error fetching customers."}, status=status.HTTP_400_BAD_REQUEST)




@login_required
@api_view(['POST'])
@check_permissions(IsAdministrator)
def add_airline_api(request):
    try:

        data = request.data.copy()  # Get a mutable copy of the data

        # Ensure country_id and user_id are integers
        if 'country_id' in data:
            data['country_id'] = int(data['country_id'])
        if 'user_id' in data:
            data['user_id'] = int(data['user_id'])


        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        airline = facade.add_airline(request.data)
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
    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
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
    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        facade.remove_customer({"id": customer_id})
        logger.info(f"Successfully removed customer with ID: {customer_id}.")
        return Response({"message": "Customer successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing customer: {str(e)}")
        return Response({"error": "Error removing customer."}, status=status.HTTP_400_BAD_REQUEST)






@login_required
@login_required
@api_view(['DELETE'])
@check_permissions(IsAdministrator)
def remove_administrator_api(request, admin_id):
    print(request.session.get('login_token'))

    try:
        facade = AdministratorFacade(request, request.user, get_login_token_from_request(request))
        facade.remove_administrator({"id": admin_id})
        logger.info(f"Successfully removed administrator with ID: {admin_id}.")
        return Response({"message": "Administrator successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing administrator: {str(e)}")
        return Response({"error": "Error removing administrator."}, status=status.HTTP_400_BAD_REQUEST)
