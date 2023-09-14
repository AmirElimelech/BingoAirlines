
import decimal
import logging
from django.utils import timezone
from .facade_base import FacadeBase
from django.core.mail import send_mail
from ..utils.login_token import LoginToken
from django.core.exceptions import ValidationError
from ..models import Customers, Tickets, Flights , Booking , Airport , Airline_Companies , Booking , DAL



logger = logging.getLogger(__name__)




class CustomerFacade(FacadeBase):

    """
    Initialize the CustomerFacade object with request, user, and an optional login token.
    Inherits from the FacadeBase class.
    """
    
    def __init__(self, request, user, login_token: LoginToken=None):
        super().__init__(request, login_token)
        self.user = user


################################ Helper and Auth Methods ################################


    def validate_customer_privileges(self):

        """
        Ensure that the user possesses the necessary customer role to perform specific operations.
        Raises an error if the user's role is not 'customer'.
        """

        user_role = self.login_token.user_role
        if user_role != "customer":
            logging.info("User does not have the necessary privileges to perform this operation.")
            raise PermissionError("You do not have the necessary privileges to perform this operation.")
        



    def validate_booking_data(self, data):
        """
        Validate the booking data provided.
        """

        # Check for booking_date
        if not data.get("booking_date"):
            raise ValidationError("Booking date is required.")

        # Validate total_price
        total_price = data.get('total_price', None)
        if total_price is None or not isinstance(total_price, (float, decimal.Decimal)):
            raise ValidationError("Total price should be a valid number.")

        # Check for flight_number
        if not data.get("flight_number"):
            raise ValidationError("Flight number is required.")

        # Validate origin and destination airport codes
        origin_airport = data.get("origin_airport", {})
        destination_airport = data.get("destination_airport", {})

        if not origin_airport.get("iataCode") or not destination_airport.get("iataCode"):
            raise ValidationError("Both origin and destination airport codes are required.")
        



    def send_email_to_user(self, subject, message, recipient_email):
        try:
            send_mail(
                subject,
                '',  # Empty plain text message
                'Bingo Airlines Info <BingoAirlines.info@gmail.com>',
                [recipient_email],
                fail_silently=False,
                html_message=message  # Send the message as HTML content
            )
            logging.info(f"Successfully sent email to {recipient_email}")
        except Exception as e:
            logging.error(f"Error sending email to {recipient_email}: {e}")







################################### CUSTOMER Methods  ###################################


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
            # Get the related Customers record
            customer = self.user.customers_set.first()  
            return self.DAL.get_tickets_by_customer(customer.id)
        except Exception as e:
            logging.error(f"Error fetching tickets for the customer: {e}")
            raise




    def get_my_bookings(self, booking_id=None):
        """
        Retrieve all flight bookings or a single booking associated with the current customer.
        """
        bookings_details = self.DAL.get_bookings_by_customer(self.user.customers_set.first().id, booking_id)
        return bookings_details


    




    def create_booking(self, data):
        # Validate data
        self.validate_booking_data(data)

        try:
            # Assuming that the customer is associated with the logged-in user
            customer_instance = self.DAL.get_by_id(Customers, self.user.id, "user_id")

            # Create or update Flight instance
            flight_instance = self.DAL.get_by_id(Flights, data["flight_number"], "flight_number")
        
            if not flight_instance:
                origin_airport_instance = self.DAL.get_by_id(Airport, data["origin_airport"]["iataCode"], "iata_code")
                destination_airport_instance = self.DAL.get_by_id(Airport, data["destination_airport"]["iataCode"], "iata_code")
                airline_company_instance = self.DAL.get_by_id(Airline_Companies, data["airline"]["iataCode"], "iata_code")

                flight_instance = self.DAL.add(
                    Flights, 
                    flight_number=data["flight_number"],
                    origin_airport=origin_airport_instance,
                    destination_airport=destination_airport_instance,
                    departure_time=data["departure_time"],
                    landing_time=data["landing_time"],
                    departure_terminal=data.get("departure_terminal"),  # Using .get() to handle optional fields
                    arrival_terminal=data.get("arrival_terminal"),
                    airline_company_id=airline_company_instance,
                    remaining_tickets=data["remaining_tickets"]  # Assuming new flights have the provided number of tickets
                )

            # Create Booking instance
            booking_instance = self.DAL.add(
                Booking, 
                booking_date=data["booking_date"], 
                total_price=data["total_price"], 
                customer=customer_instance
            )

            # Create Ticket instance
            ticket_instance = self.DAL.add(
                Tickets, 
                flight_number_ref=flight_instance,
                customer_id=customer_instance,
                Booking=booking_instance,
                currency=data["currency"],
                cabin=data["cabin"],
                adult_traveler_count=data["adult_traveler_count"],
                child_traveler_count=data["child_traveler_count"]
            )

            return {"message": "Booking successfully created."}

        except Exception as e:
            raise ValueError(f"Error creating booking: {str(e)}")



        

    

    def delete_booking(self, booking_id):
        try:
            # Initialize the DAL
            dal = DAL()

            # Use DAL's get_by_id method to fetch the booking
            booking = dal.get_by_id(Booking, booking_id)

            # Fetch the associated customer for the current user
            associated_customer = dal.get_by_id(Customers, self.user.id, field_name="user_id")

            # Check if booking belongs to the customer
            if booking and booking.customer == associated_customer:
                # Use the DAL remove method to delete the booking
                dal.remove(booking)
                logger.info(f"Successfully deleted booking {booking_id}")
                return True
            else:
                logger.error(f"Booking {booking_id} not found or does not belong to customer {self.user.username}")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting booking {booking_id}: {str(e)}") 
            return False

