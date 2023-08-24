
import  logging
from rest_framework import    status
from ..serializers import FlightsSerializer
from rest_framework.response import   Response
from Api.permissions     import    IsAirlineCompany
from rest_framework.decorators     import     api_view
from Bingo.facades.airline_facade  import    AirlineFacade
from Bingo.decorators import check_permissions , login_required






logger = logging.getLogger(__name__)






@login_required
@api_view(['GET'])
@check_permissions(IsAirlineCompany)
def get_my_flights_api(request):

    """
    Get all flights of the logged in Airline Company.
    """
    
    try:
        login_token = request.session.get('login_token')  # Extract the login token from the session
        facade = AirlineFacade(request, request.user, login_token)  # Initialize the facade with the login token
        flights = facade.get_my_flights()

        serializer = FlightsSerializer(flights, many=True)
        if not flights:
            logger.info(f"No flights found for airline company {request.user}.")
            return Response({"message": f"No flights found for airline company {request.user}."}, status=status.HTTP_200_OK)
        
        logger.info(f"Successfully fetched flights for airline company {request.user}.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching flights: {str(e)}")
        return Response({"error": "Error fetching flights."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@login_required
@api_view(['POST'])
@check_permissions(IsAirlineCompany)
def add_flight_api(request):

    """
    Add a flight to the database of the logged in Airline Company .
    """

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

    """
    Update a flight in the database of the logged in Airline Company .
    """

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

    """
    Remove a flight from the database of the logged in Airline Company .
    """

    try:
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user , login_token_dict)
        facade.remove_flight({"id": flight_id})
        logger.info(f"Successfully removed flight with ID: {flight_id}.")
        return Response({"message": "Flight successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing flight: {str(e)}")
        return Response({"error": "Error removing flight."}, status=status.HTTP_400_BAD_REQUEST)
