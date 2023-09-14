
import logging
from rest_framework import status
from Api.permissions import IsCustomer
from rest_framework.response import Response
from rest_framework.decorators import api_view 
from Bingo.models import Customers, DAL , Tickets
from Api.serializers import BookingCreateSerializer
from django.contrib.auth.models import AnonymousUser
from Bingo.utils.format_datetime import format_datetime
from Bingo.facades.customer_facade import CustomerFacade
from django.contrib.auth.decorators import login_required
from Bingo.decorators import check_permissions , login_required
from ..serializers import TicketsSerializer, CustomersSerializer , BookingDetailSerializer








logger = logging.getLogger(__name__)


 

@api_view(['PUT'])
@login_required
@check_permissions(IsCustomer)
def update_customer_api(request):
    # Print the entire request payload to the terminal
    logger.info(f"update_customer_api - Request payload: {request.data}")

     # Log the current user and their authentication status
    logger.info(f"User: {request.user.username}") 


    # Log the current session's login token
    login_token = request.session.get('login_token', None)
    logger.info(f"update_customer_api - Login token from session: {login_token}")

    """
    Update the details of the logged in customer.
    """

    # Extract phone number from request data
    phone_no = request.data.get('phone_no')

    # Check if phone number exists for another customer
    existing_customer = Customers.objects.filter(phone_no=phone_no).exclude(user_id=request.user.id).first()
    if existing_customer:
        return Response({"error": "Phone number already exists!"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        facade = CustomerFacade(request, request.user)
        updated_customer = facade.update_customer(request.data)
        serializer = CustomersSerializer(updated_customer)
        logger.info("update_customer_api - Customer details successfully updated.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"update_customer_api - Error updating customer details: {str(e)}")
        return Response({"error": "Error updating customer details."}, status=status.HTTP_400_BAD_REQUEST)




@login_required
@api_view(['POST'])
@check_permissions(IsCustomer)
def add_ticket_api(request):

    """
    Add a ticket to the database of the logged in customer.
    """

    try:
        facade = CustomerFacade(request, request.user)
        ticket = facade.add_ticket(request.data)
        serializer = TicketsSerializer(ticket)
        logger.info("Ticket successfully added.")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"Error adding ticket: {str(e)}")
        return Response({"error": "Error adding ticket."}, status=status.HTTP_400_BAD_REQUEST)




@login_required
@api_view(['DELETE'])
@check_permissions(IsCustomer)
def remove_ticket_api(request, ticket_id):

    """
    Remove a ticket from the database of the logged in customer.
    """

    try:
        facade = CustomerFacade(request, request.user)
        facade.remove_ticket(ticket_id)
        logger.info(f"Ticket with id {ticket_id} removed.")
        return Response({"message": "Ticket successfully removed."}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        logger.error(f"Error removing ticket: {str(e)}")
        return Response({"error": "Error removing ticket."}, status=status.HTTP_400_BAD_REQUEST)




@login_required
@api_view(['GET'])
@check_permissions(IsCustomer)
def get_my_tickets_api(request):

    """
    Get all tickets of the logged in customer.
    """
    
    
    try:
        login_token = request.session.get('login_token')  # Extract the login token from the session
        facade = CustomerFacade(request, request.user, login_token)  # Initialize the facade with the login token
        tickets = facade.get_my_tickets()

        serializer = TicketsSerializer(tickets, many=True)
        if not tickets:
            logger.info("No tickets found for the customer.")
            return Response({"message": f"No tickets found for {request.user}"}, status=status.HTTP_200_OK)
        
        logger.info(f"Successfully fetched customer {request.user} tickets.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        return Response({"error": "Error fetching tickets."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@login_required
@api_view(['GET'])
@check_permissions(IsCustomer)
def get_my_bookings_api(request, booking_id=None):
    """
    Get all bookings of the logged in customer.
    """
    try:
        # Extract the login token from the session
        login_token = request.session.get('login_token')
        
        # Initialize the facade with the login token
        facade = CustomerFacade(request, request.user, login_token)
        
        bookings = facade.get_my_bookings(booking_id)

        if not bookings:
            logger.info("No bookings found for the customer.")
            return Response({"message": f"No bookings found for {request.user}"}, status=status.HTTP_200_OK)
        
        # Serialize the bookings using the BookingDetailSerializer
        serializer = BookingDetailSerializer(bookings, many=True)
        serialized_bookings = serializer.data
        
        logger.info(f"Successfully fetched customer {request.user} bookings.")
        return Response(serialized_bookings, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        return Response({"error": "Error fetching bookings."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['POST'])
@login_required
@check_permissions(IsCustomer)
def create_booking(request):
    """
    Handles the flight booking process for authenticated users.
    """

    # Log the incoming request payload
    logger.info(f"create_booking - Request payload: {request.data}")

    # Log the current user and their authentication status
    logger.info(f"User: {request.user.username}") 

    # Log the current session's login token
    login_token = request.session.get('login_token', None)
    logger.info(f"create_booking - Login token from session: {login_token}")

    # Check if the request.user is an instance of AnonymousUser
    if isinstance(request.user, AnonymousUser):
        logger.error("create_booking - User is not authenticated.")
        return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

    # Fetch the customer associated with the current user.
    customer = Customers.objects.get(user_id=request.user.id)

    segments = request.data.get('segments', [])

    for segment in segments:

        # Check if the user has already booked this flight by checking the Tickets model
        existing_ticket = Tickets.objects.filter(
            flight_number_ref__flight_number=segment['flight_number'],
            customer_id=customer
        ).first()

        if existing_ticket:
            logger.error(f"create_booking - Flight {segment['flight_number']} already booked by user {request.user.username}")
            return Response({"error": f"You have already booked flight {segment['flight_number']}. Please check your bookings."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate incoming data using the serializer
        serializer = BookingCreateSerializer(data=segment)
        if not serializer.is_valid():
            logger.error(f"create_booking - Invalid data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            facade = CustomerFacade(request, request.user)
            response_data = facade.create_booking(serializer.validated_data)
            logger.info("create_booking - Booking successfully created.")
        except ValueError as e:
            logger.error(f"create_booking - Error creating booking: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    user_email = request.user.email
    subject = "Your Flight Booking Confirmation"
    message = "Dear {},\n\nThank you for booking your flight(s) with BingoAirlines.\n\n".format(request.user.username)

    dal = DAL()  # instantiate DAL


    for segment in segments:
        origin_name = dal.get_airport_name_by_iata(segment['origin_airport']['iataCode'])
        destination_name = dal.get_airport_name_by_iata(segment['destination_airport']['iataCode'])

        departure_date, departure_time = format_datetime(segment['departure_time'])
        landing_date, landing_time = format_datetime(segment['landing_time'])

        message += "Flight Number: {}\n".format(segment['flight_number'])
        message += "From: **({})** {} on {} at {}\n".format(segment['origin_airport']['iataCode'], origin_name, departure_date, departure_time)
        message += "To: **({})** {} on {} at {}\n\n".format(segment['destination_airport']['iataCode'], destination_name, landing_date, landing_time)

    message += "Safe travels!\nBingoAirlines Team"

    facade.send_email_to_user(subject, message, user_email)    

    return Response({"message": "Booking successfully created for all segments."}, status=status.HTTP_201_CREATED)




@api_view(['DELETE'])
@login_required
@check_permissions(IsCustomer)
def delete_booking(request, booking_id):
    """
    Deletes a booking and its associated tickets for the authenticated Customer .
    
    """
    try:
        facade = CustomerFacade(request, request.user)
        success = facade.delete_booking(booking_id)
        
        if success:
            return Response({"message": f"Booking {booking_id} successfully deleted."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"Failed to delete Booking {booking_id}."}, status=status.HTTP_400_BAD_REQUEST)
    
    except ValueError as e:
        logger.error(f"delete_booking - Error deleting booking {booking_id}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)