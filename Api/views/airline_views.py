from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import FlightsSerializer
from Bingo.facades.airline_facade import AirlineFacade
from django.views.decorators.csrf import csrf_exempt
from Bingo.decorators import check_permissions , login_required
from Api.permissions import IsAirlineCompany
import logging


logger = logging.getLogger(__name__)


@login_required
@api_view(['GET'])
@check_permissions(IsAirlineCompany)
def get_my_flights_api(request):
    logger.info(f"In get_my_flights_api with user: {request.user}")
    
    try:
        login_token = request.session.get('login_token')  # Extract the login token from the session
        facade = AirlineFacade(request, request.user, login_token)  # Initialize the facade with the login token
        flights = facade.get_my_flights()

        if not flights:
            return Response({"erorr": "Could not fetch flights for the user."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = FlightsSerializer(flights, many=True)
        logger.info("Successfully fetched airline's flights.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching flights: {str(e)}")
        return Response({"error": "Error fetching flights."}, status=status.HTTP_400_BAD_REQUEST)


@login_required
@api_view(['POST'])
@check_permissions(IsAirlineCompany)
def add_flight_api(request):
    try:
        # Extract login token or user details from the request
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user, login_token_dict)
        flight = facade.add_flight(request.data)
        serializer = FlightsSerializer(flight)
        logger.info("Successfully added flight.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding flight: {str(e)}")
        return Response({"error": "Error adding flight."}, status=status.HTTP_400_BAD_REQUEST)



@login_required
@api_view(['PUT'])
@check_permissions(IsAirlineCompany)
def update_flight_api(request):
    try:
        # Extract login token or user details from the request
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user, login_token_dict)
        flight = facade.update_flight(request.data)
        serializer = FlightsSerializer(flight)
        logger.info("Successfully updated flight.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating flight: {str(e)}")
        return Response({"error": "Error updating flight."}, status=status.HTTP_400_BAD_REQUEST)

@login_required
@api_view(['DELETE'])
@check_permissions(IsAirlineCompany)
def remove_flight_api(request, flight_id):
    try:
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user , login_token_dict)
        facade.remove_flight({"id": flight_id})
        logger.info(f"Successfully removed flight with ID: {flight_id}.")
        return Response({"message": "Flight successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing flight: {str(e)}")
        return Response({"error": "Error removing flight."}, status=status.HTTP_400_BAD_REQUEST)
