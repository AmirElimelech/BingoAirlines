
import logging
from rest_framework import status
from Api.permissions import IsCustomer
from Bingo.models import Customers, DAL
from rest_framework.response import Response
from Bingo.facades.customer_facade import CustomerFacade
from rest_framework.parsers import MultiPartParser, FormParser 
from Bingo.decorators import check_permissions , login_required
from rest_framework.decorators import api_view , parser_classes 
from ..serializers import TicketsSerializer, CustomersSerializer , BookingDetailSerializer
from django.views.decorators.csrf import csrf_exempt




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
def get_my_bookings_api(request):

    """
    Get all bookings of the logged in customer.
    """
    
    try:
        login_token = request.session.get('login_token')  # Extract the login token from the session
        facade = CustomerFacade(request, request.user, login_token)  # Initialize the facade with the login token
        bookings = facade.get_my_bookings()

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
