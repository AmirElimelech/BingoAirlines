
import logging
from rest_framework import status
from Api.permissions import IsCustomer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Bingo.facades.customer_facade import CustomerFacade
from Bingo.decorators import check_permissions , login_required
from ..serializers import TicketsSerializer, CustomersSerializer






logger = logging.getLogger(__name__)




@login_required
@api_view(['PUT'])
@check_permissions(IsCustomer)
def update_customer_api(request):

    """
    Update the details of the logged in customer.
    """

    try:
        facade = CustomerFacade(request, request.user)
        updated_customer = facade.update_customer(request.data)
        serializer = CustomersSerializer(updated_customer)
        logger.info("Customer details successfully updated.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error updating customer details: {str(e)}")
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
    
    logger.info(f"In get_my_tickets_api with user: {request.user}")
    
    try:
        login_token = request.session.get('login_token')  # Extract the login token from the session
        facade = CustomerFacade(request, request.user, login_token)  # Initialize the facade with the login token
        tickets = facade.get_my_tickets()

        if not tickets:
            return Response({"error": "Could not fetch tickets for the user."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TicketsSerializer(tickets, many=True)
        logger.info("Successfully fetched customer's tickets.")
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error fetching tickets: {str(e)}")
        return Response({"error": "Error fetching tickets."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
