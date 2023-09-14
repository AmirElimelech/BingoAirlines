
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
def get_my_flights_api(request, flight_id=None):
    """
    Get all flights of the logged in Airline Company or a specific flight.
    """
    try:
        login_token = request.session.get('login_token')
        facade = AirlineFacade(request, request.user, login_token)
        flights = facade.get_my_flights_new(flight_id)

        if flight_id:
            # If fetching a single flight, don't use many=True
            serializer = FlightsSerializer(flights)
        else:
            serializer = FlightsSerializer(flights, many=True)

        if not flights:
            logger.info(f"No flights found for airline company {request.user}.")
            return Response({"message": f"No flights found for airline company {request.user}."}, status=status.HTTP_200_OK)
        
        logger.info(f"Successfully fetched flights for airline company {request.user}.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching flights: {str(e)}")
        return Response({"error": "Error fetching flights."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@login_required
@check_permissions(IsAirlineCompany)
def add_flight_api(request):
    """
    Add a flight to the database of the logged in Airline Company.
    """
    try:
        # Extract login token or user details from the request
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user, login_token_dict)

        # Fetch the airline company associated with the logged-in user
        airline_company = facade.validate_airline_privileges()

        # Update the payload with the correct iata_code
        updated_data = request.data
        updated_data['airline_company_id'] = airline_company.iata_code

        # Prepend the IATA code to the flight number
        updated_data['flight_number'] = airline_company.iata_code + updated_data['flight_number']

        flight = facade.add_flight(updated_data)
        serializer = FlightsSerializer(flight)
        logger.info("Successfully added flight.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding flight: {str(e)}")
        return Response({"error": "Error adding flight."}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['PUT'])
@login_required
@check_permissions(IsAirlineCompany)
def update_flight_api(request):

    """
    Update a flight in the database of the logged in Airline Company.
    """

    try:
        # Extract login token or user details from the request
        login_token_dict = request.session.get('login_token')
        facade = AirlineFacade(request, request.user, login_token_dict)

        # Fetch the airline company associated with the logged-in user
        airline_company = facade.validate_airline_privileges()

        # Update the payload with the correct iata_code
        updated_data = request.data
        updated_data['airline_company_id'] = airline_company.iata_code

        flight = facade.update_flight(updated_data)
        serializer = FlightsSerializer(flight)
        logger.info("Successfully updated flight.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating flight: {str(e)}")
        return Response({"error": "Error updating flight."}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
@login_required
@check_permissions(IsAirlineCompany)
def remove_flight_api(request, flight_id):
    """
    Remove a flight from the database of the logged in Airline Company.
    """
    try:
        # Get the login_token_dict from the session
        login_token_dict = request.session.get('login_token')
        
        # Initialize the AirlineFacade with the login_token_dict
        facade = AirlineFacade(request, request.user, login_token_dict)
        
        facade.remove_flight({"id": flight_id})
        logger.info(f"Successfully removed flight with ID: {flight_id}.")
        return Response({"message": "Flight successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing flight: {str(e)}")
        return Response({"error": "Error removing flight."}, status=status.HTTP_400_BAD_REQUEST)

