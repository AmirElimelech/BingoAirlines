from django.shortcuts import render, redirect
from django.http import JsonResponse
from ..models import DAL, Flights, Tickets, Customers , Users
from ..decorators import login_required
from ..forms import CustomerForm, UsersForm
from ..utils.login_token import LoginToken 
import logging
from django.urls import reverse
from .base_views import BaseViews



logger = logging.getLogger(__name__)
dal = DAL()

class CustomerViews(BaseViews):


    # @staticmethod
    # @login_required
    # def update_customer_view(request, customer_id):
    #     # Validation
    #     CustomerViews.validate_login_token_and_role(request)
    #     # First, we need to get the current customer
    #     customer_instance = dal.get_by_id(Customers, customer_id)

    #     # Check if the customer exists
    #     if not customer_instance:
    #         log.error(f"Customer with ID {customer_id} not found.")
    #         return JsonResponse({"error": "Customer not found."}, status=404)

    #     user_form = UsersForm(request.POST or None, request.FILES or None, instance=customer_instance.user_id)
    #     customer_form = CustomerForm(request.POST or None, instance=customer_instance)

    #     if request.method == "POST" and user_form.is_valid() and customer_form.is_valid():
    #         user_data = {
    #             "id": user_form.cleaned_data.get("id"),
    #             "username": user_form.cleaned_data.get("username"),
    #             "email": user_form.cleaned_data.get("email"),
    #             "password": user_form.cleaned_data.get("password"),
    #             "user_role": user_form.cleaned_data.get("user_role"),
    #             "image": user_form.cleaned_data.get("image"),
    #         }

    #         customer_data = {
    #             'user_id': customer_instance.user_id.id,
    #             'first_name': customer_form.cleaned_data.get("first_name"),
    #             'last_name': customer_form.cleaned_data.get("last_name"),
    #             'address': customer_form.cleaned_data.get("address"),
    #             'phone_no': customer_form.cleaned_data.get("phone_no"),
    #             'credit_card_no': customer_form.cleaned_data.get("credit_card_no")
    #         }

    #         try:
    #             dal.update(Users, **user_data)
    #             dal.update(Customers, **customer_data)
    #             log.info(f"Customer with ID {customer_id} updated successfully.")
    #             return JsonResponse({"message": "Customer updated successfully."})

    #         except Exception as e:
    #             log.error(f"Error during customer update: {str(e)}")
    #             return JsonResponse({"error": "An error occurred during update."}, status=400)

    #     context = {
    #         'user_form': user_form,
    #         'customer_form': customer_form,
    #         'user_role': "Customer"
    #     }
    #     return render(request, 'register.html', context)


    @staticmethod
    @login_required
    def update_customer_view(request):
        # Validation
        try:
            login_token = LoginToken.validate_login_token(request)
            if login_token.user_role != "Customer":
                raise PermissionError("You do not have the necessary privileges.")
        except PermissionError:
            return redirect(reverse('home'))

        # Get the customer instance associated with the logged-in user
        customer_instance = DAL.get_by_id(Customers, login_token.user_id)

        # If the customer doesn't exist, redirect to home
        if not customer_instance:
            logger.error(f"No customer associated with user ID: {login_token.user_id}")
            return redirect(reverse('home'))

        # Handle form submission
        if request.method == "POST":
            form = CustomerForm(request.POST, instance=customer_instance)
            if form.is_valid():
                DAL.update(customer_instance, **form.cleaned_data)
                logger.info(f"Successfully updated customer: {customer_instance.first_name} {customer_instance.last_name}")
                return redirect(reverse('home'))
            else:
                logger.error("Form errors while updating customer:", form.errors)
        else:
            form = CustomerForm(instance=customer_instance)

        return render(request, "update_customer.html", {"form": form})
    



    @staticmethod
    @login_required
    def add_ticket_view(request, flight_id):
        CustomerViews.validate_login_token_and_role(request)
        flight = dal.get_by_id(Flights, flight_id)
        if flight.remaining_tickets <= 0:
            logger.error(f"No available tickets for flight with ID {flight_id}.")
            return JsonResponse({"error": "Sorry, this flight is fully booked."}, status=400)
        
        ticket_data = {
            'customer_id': request.user.customer.id,
            'flight_id': flight_id
        }
        try:
            ticket_instance = dal.add(Tickets, **ticket_data)
            logger.info(f"Added ticket for customer {request.user.username} for flight ID {flight_id}.")
            return JsonResponse({"message": "Ticket booked successfully."})
        except Exception as e:
            logger.error(f"Error while adding ticket: {str(e)}")
            return JsonResponse({"error": "An error occurred while booking ticket."}, status=400)

    @staticmethod
    @login_required
    def remove_ticket_view(request, ticket_id):
        CustomerViews.validate_login_token_and_role(request)
        ticket_instance = dal.get_by_id(Tickets, ticket_id)

        if not ticket_instance:
            logger.error(f"Ticket with ID {ticket_id} not found.")
            return JsonResponse({"error": "Ticket not found."}, status=404)

        if ticket_instance.customer_id != request.user.customer.id:
            logger.error(f"Unauthorized removal attempt of ticket {ticket_id} by user {request.user.username}.")
            return JsonResponse({"error": "You can only remove your own tickets."}, status=403)

        try:
            dal.remove(ticket_instance)
            logger.info(f"Ticket with ID {ticket_id} removed successfully.")
            return JsonResponse({"message": "Ticket removed successfully."})
        except Exception as e:
            logger.error(f"Error while removing ticket: {str(e)}")
            return JsonResponse({"error": "An error occurred while removing ticket."}, status=400)

    @staticmethod
    @login_required
    def get_my_tickets_view(request):
        CustomerViews.validate_login_token_and_role(request)
        tickets = dal.get_tickets_by_customer(request.user.customer.id)
        return JsonResponse({"tickets": [ticket.serialize() for ticket in tickets]})
