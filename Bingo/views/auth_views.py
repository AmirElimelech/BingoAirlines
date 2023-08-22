# IMPORTS

import logging

from django.urls import reverse
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render , redirect
from django.core.exceptions import ValidationError
from django.contrib.auth import logout as django_logout

from Bingo.facades.airline_facade import AirlineFacade
from Bingo.facades.customer_facade import CustomerFacade
from Bingo.facades.anonymous_facade import AnonymousFacade 
from Bingo.facades.administrator_facade import AdministratorFacade

from ..decorators import login_required
from ..utils.login_token import LoginToken
from ..facades.facade_base import FacadeBase 
from ..models import User_Roles , Users , User_Roles , DAL
from ..forms import UsersForm , CustomerForm , AdministratorForm , AirlineCompanyForm






# logger 

logger = logging.getLogger(__name__)




def home_view(request):

    """
    Home view for the BingoAirlines project.
    """

    # Initialize user as None
    user = None

    try:
        # Fetch the user using the login_token stored in the session
        login_token = request.session.get('login_token')

        if login_token:
            dal_instance = DAL()
            user = dal_instance.get_by_id(Users, login_token["user_id"])

            # Check user roles and initialize the corresponding facade
            if login_token["user_role"] == 'customer':
                facade = CustomerFacade(request, user, login_token)
            elif login_token["user_role"] == 'airline company':
                facade = AirlineFacade(request, user, login_token)  # Assuming you have a similar structure for AirlineFacade
            elif login_token["user_role"] == 'administrator':
                facade = AdministratorFacade(request, user, login_token)  # Assuming you have a similar structure for AdministratorFacade
            else:
                facade = FacadeBase(request, login_token)
    except Exception as e:
        # Optionally log the error message for debugging purposes
        logger.error(f"Error in home_view: {str(e)}")
        # Set user to None to ensure it doesn't carry any unexpected value
        user = None

    return render(request, 'home.html', {'user': user})





def user_registration_view(request):

    """
    User registration view for the BingoAirlines project , this view is used to register a new user 
    and also to register a new customer , airline company or administrator in the database.
    it is also used to redirect the user to the home page if he is already logged in.
    redirection logic is based on the user role and the user session role.

    """

    allowed_roles = ["Customer", "Airline Company", "Administrator"]

    user_role_param = request.GET.get('user_role', None)

    if user_role_param not in allowed_roles:  # Check if role is allowed
        logger.info(f"Redirecting due to invalid user role: {user_role_param}")
        return redirect('home')
    

    # Retrieve the LoginToken dictionary from the session
    login_token_dict = request.session.get('login_token')
    user_session_role = None
    if login_token_dict is not None:
        # Reconstruct the LoginToken object from the dictionary
        login_token = LoginToken(user_id=login_token_dict['user_id'], user_role=login_token_dict['user_role'])
        user_session_role = login_token.user_role


#conditions for redirection

    if user_role_param is None:
        logger.info("Redirecting due to no user role specified")
        return HttpResponseRedirect(reverse('home'))

    if user_role_param.lower() == 'customer' and user_session_role is not None and user_session_role != 'administrator':
        logger.info(f"Redirecting due to authenticated user {user_session_role.upper()} trying to access Customer registration without being an Administrator")
        return HttpResponseRedirect(reverse('home'))

    if not request.user.is_authenticated and user_role_param in ["Airline Company", "Administrator"] and user_session_role != 'administrator':
        user_session_role_str = "None" if user_session_role is None else user_session_role.upper()
        logger.info(f"Redirecting due to unauthenticated user {user_session_role_str} trying to register Airline Company or Administrator")
        return HttpResponseRedirect(reverse('home'))


    if not request.user.is_authenticated and user_role_param in ["Airline Company", "Administrator"] and user_session_role != 'administrator':
        logger.info(f"Redirecting due to unauthenticated user {user_session_role.upper()} trying to register Airline Company or Administrator")
        return HttpResponseRedirect(reverse('home'))

    user_role_instance = None
    try:
        user_role_instance = User_Roles.objects.get(role_name=user_role_param)
    except User_Roles.DoesNotExist:
        pass

    user_form = UsersForm(request.POST or None, request.FILES or None, initial={'user_role': user_role_instance})
    entity_form = None



    if user_role_param == "Customer":
        entity_form = CustomerForm(request.POST or None)
    elif user_role_param == "Airline Company":
        entity_form = AirlineCompanyForm(request.POST or None, request.FILES or None)
    elif user_role_param == "Administrator":
        entity_form = AdministratorForm(request.POST or None)

    if request.method == "POST":

        try:

            if user_form.is_valid() and (entity_form is None or entity_form.is_valid()):
                user_data = {
                    "id": user_form.cleaned_data.get("id"),
                    "username": user_form.cleaned_data.get("username"),
                    "email": user_form.cleaned_data.get("email"),
                    "password": user_form.cleaned_data.get("password"),
                    "user_role": user_form.cleaned_data.get("user_role"),
                    "image": user_form.cleaned_data.get("image"),
                }

                try:
                    with transaction.atomic():  # Transaction block starts here
                        facade = FacadeBase(request)
                        user_instance = facade.create_new_user(user_data)
                        
                        

                        if user_role_param == "Customer":
                            customer_data = {
                                'user_id': user_instance.id,
                                'first_name': entity_form.cleaned_data.get("first_name"),
                                'last_name': entity_form.cleaned_data.get("last_name"),
                                'address': entity_form.cleaned_data.get("address"),
                                'phone_no': entity_form.cleaned_data.get("phone_no"),
                                'credit_card_no': entity_form.cleaned_data.get("credit_card_no")
                            }
                            anonymous_facade = AnonymousFacade(request)
                            customer_instance = anonymous_facade.add_customer(customer_data)
                            logging.info(f"Successfully created Customer instance: {customer_instance}")

                        elif user_role_param == "Airline Company":
                            airline_data = {

                                
                                'user_id': user_instance,
                                'iata_code': entity_form.cleaned_data.get("iata_code"),
                                'name': entity_form.cleaned_data.get("name"),
                                'country_id': entity_form.cleaned_data.get("country_id"),
                                'logo': entity_form.cleaned_data.get("logo"),
                            }
                            admin_facade = AdministratorFacade(request, user_instance , login_token)
                            airline_instance = admin_facade.add_airline(airline_data)
                            logging.info(f"Successfully created Airline Company instance: {airline_instance}")


                        elif user_role_param == "Administrator":
                            admin_data = {
                            
                                
                                'user_id': user_instance,
                                'first_name': entity_form.cleaned_data.get("first_name"),
                                'last_name': entity_form.cleaned_data.get("last_name"),
                            }
                            admin_facade = AdministratorFacade(request, user_instance , login_token )
                            admin_instance = admin_facade.add_administrator(admin_data)
                            logging.info(f"Successfully created Administrator instance: {admin_instance}")

                    logging.info(f"Successfully created Users instance: {user_instance.username}")
                    return HttpResponseRedirect(reverse('login'))

                except Exception as e:  # General exception handling
                    logger.error(f"Error during registration: {str(e)}")
                    user_form.add_error(None, "An error occurred during registration. Please try againnnnn.")

            else:
                logger.error("User Form errors: %s", user_form.errors.as_text())
                if entity_form:
                    logger.error("Entity Form errors: %s", entity_form.errors.as_text())

        except Exception as e:
            logger.error(f"Exception occurred during user registration: {e}")
            user_form.add_error(None, "An unexpected error occurred during registration. Please try again.")


  

    return render(request, "register.html", {
        "user_form": user_form,
        "entity_form": entity_form,
        "user_role": user_role_param
    })



def login_view(request):

    """
    Login view for the BingoAirlines project.
    """

    try:
        login_token = request.session.get('login_token')
        if login_token and login_token.get('user_id'):
            user_id = login_token['user_id']
            user = Users.objects.get(id=user_id)

            logging.info(f"User {user.username} tried to access the login page while already logged in.")
            return redirect('home')
    except Users.DoesNotExist:
        logger.warning(f"User with ID {user_id} does not exist.")
    except Exception as e:
        logger.error(f"Error checking logged-in user: {str(e)}")

    error_message = None

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        facade = AnonymousFacade(request)

        try:
            login_token = facade.login(username, password)
            request.session['login_token'] = {'user_id': login_token.user_id, 'user_role': login_token.user_role}  # Store login_token in session
            logging.info(f"Welcome {username}! Successfully logged in as {login_token.user_role}.")
            return redirect('home')
        except ValidationError as e:
            error_message = str(e)
            logger.error(f"Login error: {error_message}")
        except Exception as e:
            error_message = "An unexpected error occurred during login."
            logger.error(f"Unexpected login error: {str(e)}")

    return render(request, 'login.html', {'error': error_message})




@login_required
def logout_view(request):

    """
    Logout view for the BingoAirlines project.
    """

    try:
        if 'login_token' in request.session:
            del request.session['login_token']
            django_logout(request)
            logging.info(f"Successfully logged out")
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        
    return redirect('login')


