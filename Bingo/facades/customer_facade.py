
import logging
from django.utils import timezone
from .facade_base import FacadeBase
from ..utils.login_token import LoginToken
from django.core.exceptions import ValidationError
from ..models import Customers, Tickets, Flights , Booking



logger = logging.getLogger(__name__)




class CustomerFacade(FacadeBase):

    """
    Initialize the CustomerFacade object with request, user, and an optional login token.
    Inherits from the FacadeBase class.
    """
    
    def __init__(self, request, user, login_token: LoginToken=None):
        super().__init__(request, login_token)
        self.user = user

    def validate_customer_privileges(self):

        """
        Ensure that the user possesses the necessary customer role to perform specific operations.
        Raises an error if the user's role is not 'customer'.
        """

        user_role = self.login_token.user_role
        if user_role != "customer":
            logging.info("User does not have the necessary privileges to perform this operation.")
            raise PermissionError("You do not have the necessary privileges to perform this operation.")


    def update_customer(self, customer):

        """
        Update an existing customer's details after validating the provided information.
        """

        # Retrieve the existing customer instance
        existing_customer = self.DAL.get_by_id(Customers, customer["id"])

        # Check if the customer exists
        if not existing_customer:
            raise ValidationError("Customer not found.")

        # Validate names
        if not customer["first_name"].isalpha() or not customer["last_name"].isalpha():
            raise ValidationError("Names should only contain letters.")
        
        # Validate address length dynamically
        max_address_length = Customers._meta.get_field('address').max_length
        if len(customer["address"]) > max_address_length:
            raise ValidationError(f"Address is too long. Maximum allowed length is {max_address_length} characters.")
        
        # Validate Credit Card Number
        card_num = customer["credit_card_no"]
        if len(card_num) not in [13, 15, 16] or not card_num.isdigit():
            raise ValidationError("Credit card number should be 13, 15, or 16 digits long.")

    
        # Update the existing customer record
        for attr, value in customer.items():
            setattr(existing_customer, attr, value)
        existing_customer.save()

        return existing_customer





    # def add_ticket(self, ticket):
    #     """
    #     Add a new flight ticket for the customer after ensuring flight availability and validating the ticket information.
    #     """
    #     try:
    #         # Retrieve the Flights instance using the provided flight number
    #         flight_instance = self.DAL.get_by_id(Flights, ticket["flight_number_ref"], field_name="flight_number")

    #         logging.info(f"Flight instance: {flight_instance}")
            
    #         if not flight_instance:
    #             raise ValidationError("Flight not found.")
                
    #         if flight_instance.remaining_tickets <= 0:
    #             raise ValidationError("Sorry, this flight is fully booked.")
            
    #         # Get the customer instance associated with the user
    #         customer_instance = Customers.objects.get(user_id=self.user)
    #         if not customer_instance:
    #             raise ValidationError("Associated customer record not found for the authenticated user.")
            
    #         # Ensure customer doesn't have a ticket for the same flight
    #         existing_ticket = self.DAL.get_tickets_by_customer(customer_instance.id).filter(flight_number_ref=flight_instance).first()
    #         if existing_ticket:
    #             raise ValidationError("You already have a ticket for this flight.")
                
    #         # Retrieve the Booking instance using the provided booking ID
    #         booking_instance = self.DAL.get_by_id(Booking, ticket["Booking"])
    #         if not booking_instance:
    #             raise ValidationError("Associated booking record not found.")
            
    #         # Replace the 'flight_number_ref' in the ticket dictionary with the flight instance
    #         ticket["flight_number_ref"] = flight_instance
    #         # Replace the 'Booking' in the ticket dictionary with the booking instance
    #         ticket["Booking"] = booking_instance
            
    #         # Add the customer instance to the ticket dictionary
    #         ticket["customer_id"] = customer_instance

    #         return self.DAL.add(Tickets, **ticket)
            
    #     except ValidationError as ve:
    #         logger.error(f"Validation Error: {ve}")
    #         raise ve
            
    #     except Exception as e:
    #         logger.error(f"Unexpected error while adding ticket: {e}")
    #         raise e


    def add_ticket(self, ticket):
        """
        Add a new flight ticket for the customer after ensuring flight availability and validating the ticket information.
        function also checks if the flight has already departed , if so it will raise an error , if not it will add the ticket ,
        and deduct the number of tickets being bought from the flight's remaining tickets ( it will check if there is enough tickets available
        for the flight) , if not it will raise an error.
        """
        try:
            # Retrieve the Flights instance using the provided flight number
            flight_instance = self.DAL.get_by_id(Flights, ticket["flight_number_ref"], field_name="flight_number")

            logging.info(f"Flight instance: {flight_instance}")
            
            if not flight_instance:
                raise ValidationError("Flight not found.")
            
            # Calculate total tickets being bought
            total_tickets_bought = ticket.get("adult_traveler_count", 0) + ticket.get("child_traveler_count", 0)

            # Ensure there are enough remaining tickets
            if flight_instance.remaining_tickets < total_tickets_bought:
                raise ValidationError(f"Sorry, only {flight_instance.remaining_tickets} tickets are available for this flight.")
            
            # Deduct the number of tickets being bought from the flight's remaining tickets
            flight_instance.remaining_tickets -= total_tickets_bought
            flight_instance.save()
            
            if flight_instance.remaining_tickets < 0:
                raise ValidationError("Sorry, this flight is fully booked.")
            
            # Get the customer instance associated with the user
            customer_instance = Customers.objects.get(user_id=self.user)
            if not customer_instance:
                raise ValidationError("Associated customer record not found for the authenticated user.")
            
            # Ensure customer doesn't have a ticket for the same flight
            existing_ticket = self.DAL.get_tickets_by_customer(customer_instance.id).filter(flight_number_ref=flight_instance).first()
            if existing_ticket:
                raise ValidationError("You already have a ticket for this flight.")
                
            # Retrieve the Booking instance using the provided booking ID
            booking_instance = self.DAL.get_by_id(Booking, ticket["Booking"])
            if not booking_instance:
                raise ValidationError("Associated booking record not found.")
            
            # Replace the 'flight_number_ref' in the ticket dictionary with the flight instance
            ticket["flight_number_ref"] = flight_instance
            # Replace the 'Booking' in the ticket dictionary with the booking instance
            ticket["Booking"] = booking_instance
            
            # Add the customer instance to the ticket dictionary
            ticket["customer_id"] = customer_instance

            return self.DAL.add(Tickets, **ticket)
            
        except ValidationError as ve:
            logger.error(f"Validation Error: {ve}")
            raise ve
            
        except Exception as e:
            logger.error(f"Unexpected error while adding ticket: {e}")
            raise e





    def remove_ticket(self, ticket_id):


        """
        Remove a flight ticket associated with the customer. Ensures the ticket exists, belongs to the user, and the flight hasn't 
        departed, and increment the number of tickets on the flight, and save the flight . 
    
        """
        try:
            ticket_instance = self.DAL.get_by_id(Tickets, ticket_id)

            # Check if ticket exists
            if not ticket_instance:
                raise ValidationError("Ticket not found.")

            # Validate that the ticket belongs to the user
            customer_instance = self.DAL.get_by_id(Customers, self.user.id, field_name="user_id")

            if ticket_instance.customer_id.id != customer_instance.id:
                raise PermissionError("You can only remove your own tickets.")

            # Check if flight has already departed
            if ticket_instance.flight_number_ref.departure_time <= timezone.now():
                raise ValidationError("You can't remove a ticket after the flight's departure.")

            # Increment the number of tickets on the flight
            flight_instance = ticket_instance.flight_number_ref
            total_tickets_being_refunded = ticket_instance.adult_traveler_count + ticket_instance.child_traveler_count
            flight_instance.remaining_tickets += total_tickets_being_refunded
            flight_instance.save()

            return self.DAL.remove(ticket_instance)

        except ValidationError as ve:
            logging.error(f"Validation error while removing ticket: {ve}")
            raise ve
        except PermissionError as pe:
            logging.error(f"Permission error while removing ticket: {pe}")
            raise pe
        except Exception as e:
            logging.error(f"Unexpected error while removing ticket: {e}")
            raise





    def get_my_tickets(self):

        """
        Retrieve all flight tickets associated with the current customer.
        """
  
        try:
            customer = self.user.customers_set.first()  # Get the related Customers record
            return self.DAL.get_tickets_by_customer(customer.id)
        except Exception as e:
            logging.error(f"Error fetching tickets for the customer: {e}")
            raise

    
    
