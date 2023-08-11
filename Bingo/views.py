
from django import forms
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render ,redirect
from .utils.amadeus import get_ticket_data
from .models import Airport , User_Roles
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
import traceback
import logging
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm 
from .facades.facade_base import FacadeBase , CustomUserCreationError
from django.core.exceptions import ValidationError
from .forms import UsersForm , CustomerForm , AdministratorForm , AirlineCompanyForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from Bingo.facades.anonymous_facade import AnonymousFacade 
from Bingo.facades.administrator_facade import AdministratorFacade
from django.contrib.auth import logout as django_logout
from .models import Users , User_Roles
from django.http import HttpResponseForbidden







# logger 
logger = logging.getLogger(__name__)

def home_view(request):
    # Fetch the user using the user_id stored in the session
    user_id = request.session.get('user_id')
    if user_id:
        user = Users.objects.get(id=user_id)
    else:
        user = None

    # Pass the user to the template context
    return render(request, 'home.html', {'user': user})




def user_registration_view(request):
    user_role_param = request.GET.get('user_role', None)
    user_session_role = request.session.get('user_role')

    

    # Redirect to home page if no user role is specified
    if user_role_param is None:
        logger.info("Redirecting due to no user role specified")
        return HttpResponseRedirect(reverse('home'))

    # Redirect if the user is authenticated and not an Administrator, and they're trying to access Customer registration
    if user_role_param.lower() == 'customer' and user_session_role is not None and user_session_role != 'administrator':
        logger.info(f"Redirecting due to authenticated user {user_session_role.upper()} trying to access Customer registration without being an Administrator")
        return HttpResponseRedirect(reverse('home'))

    # If the user is authenticated and their role is Customer or Airline Company, redirect to home
    if request.user.is_authenticated and user_session_role in ['customer', 'airline company']:
        logger.info(f"Redirecting due to authenticated user with role {user_session_role.upper()} cannot register a new user")
        return HttpResponseRedirect(reverse('home'))

    # If the user is not authenticated and trying to register an Airline Company or Administrator,
    # and the user is not an Administrator, redirect to home
    if not request.user.is_authenticated and user_role_param in ["Airline Company", "Administrator"] and user_session_role != 'administrator':
        logger.info(f"Redirecting due to unauthenticated user {user_session_role.upper()} trying to register Airline Company or Administrator")
        return HttpResponseRedirect(reverse('home'))



    # Fetch the actual model instance for user_role
    user_role_instance = None
    try:
        user_role_instance = User_Roles.objects.get(role_name=user_role_param)
    except User_Roles.DoesNotExist:
        pass

    user_form = UsersForm(request.POST or None, request.FILES or None, initial={'user_role': user_role_instance})
    entity_form = None  # This form will vary based on user role

    if user_role_param == "Customer":
        entity_form = CustomerForm(request.POST or None)
    elif user_role_param == "Airline Company":
        entity_form = AirlineCompanyForm(request.POST or None, request.FILES or None)
    elif user_role_param == "Administrator":
        entity_form = AdministratorForm(request.POST or None)

    if request.method == "POST":
        if user_form.is_valid() and (entity_form is None or entity_form.is_valid()):
            facade = FacadeBase()

            user_data = {
                "id": user_form.cleaned_data.get("id"),
                "username": user_form.cleaned_data.get("username"),
                "email": user_form.cleaned_data.get("email"),
                "password": user_form.cleaned_data.get("password"),
                "user_role": user_form.cleaned_data.get("user_role"),
                "image": user_form.cleaned_data.get("image"),
            }

            try:
                user_instance = facade.create_new_user(user_data)
                
                # If we're registering a customer
                if user_role_param == "Customer":
                    customer_data = {
                        'user_id': user_instance.id, 
                        'first_name': entity_form.cleaned_data.get("first_name"),
                        'last_name': entity_form.cleaned_data.get("last_name"),
                        'address': entity_form.cleaned_data.get("address"),
                        'phone_no': entity_form.cleaned_data.get("phone_no"),
                        'credit_card_no': entity_form.cleaned_data.get("credit_card_no")
                    }
                    anonymous_facade = AnonymousFacade()
                    anonymous_facade.add_customer(customer_data)

                # If we're registering an airline company
                elif user_role_param == "Airline Company":
                    airline_data = {
                        'user_id': user_instance,
                        'iata_code': entity_form.cleaned_data.get("iata_code"),
                        'name': entity_form.cleaned_data.get("name"),
                        'country_id': entity_form.cleaned_data.get("country_id"),
                        'logo': entity_form.cleaned_data.get("logo"),
                    }
                    admin_facade = AdministratorFacade(request, user_instance)
                    admin_facade.add_airline(airline_data)

                # If we're registering an administrator
                elif user_role_param == "Administrator":
                    admin_data = {
                        'user_id': user_instance.id,
                        'first_name': entity_form.cleaned_data.get("first_name"),
                        'last_name': entity_form.cleaned_data.get("last_name"),
                    }
                    anonymous_facade = AnonymousFacade()
                    anonymous_facade.add_administrator(admin_data)

                return HttpResponseRedirect(reverse('login'))

            except ValidationError as ve:
                user_form.add_error(None, ve)
            except CustomUserCreationError as e:
                for field, error_msg in e.errors.items():
                    if field in user_form.fields:
                        user_form.add_error(field, error_msg)
                    elif entity_form and field in entity_form.fields:
                        entity_form.add_error(field, error_msg)

        else:
            logger.error("User Form errors: %s", user_form.errors.as_text())
            if entity_form:
                logger.error("Entity Form errors: %s", entity_form.errors.as_text())

    return render(request, "register.html", {
        "user_form": user_form,
        "entity_form": entity_form,
        "user_role": user_role_param
    })




def login_view(request):
    error_message = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        facade = AnonymousFacade()
        
        try:
            user_role, user_id = facade.login(request, username, password)
            return redirect('home')
        except ValidationError as e:
            error_message = str(e)
            logger.error(f"Login error: {error_message}")

    return render(request, 'login.html', {'error': error_message})



# def logout_view(request):
#     # Clear the session
#     request.session.flush()
    
#     # Call Django's logout function to ensure any other cleanup is done
#     django_logout(request)
    
#     # Redirect the user to the login page
#     return redirect('login')


def logout_view(request):
    # Clear the session
    request.session.flush()
    
    # Call Django's logout function to ensure any other cleanup is done
    from django.contrib.auth import logout as django_logout
    django_logout(request)
    
    # Redirect the user to the login page
    return redirect('login')


class SearchForm(forms.Form):
    numAdults = forms.IntegerField(min_value=1, initial=1 , label='Adults')
    numChildren = forms.IntegerField(min_value=0, initial=0 , label='Children')
    cabinType = forms.ChoiceField(choices=[('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First')] , label='Cabin Type')
    currencyCode = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('ILS', 'ILS')] , label='Currency')
    originLocationCode = forms.CharField(label='Flying From') 
    destinationLocationCode = forms.CharField(label='Flying To')
    departureDate1 = forms.DateField(label='Departure Date')
    flightType = forms.ChoiceField(choices=[('OneWay', 'One Way'), ('Return', 'Return Flight')] , label='Flight Type')
    departureDate2 = forms.DateField(required=False , label='Return Date')

    def clean(self):
        cleaned_data = super().clean()
        departureDate1 = cleaned_data.get('departureDate1')
        departureDate2 = cleaned_data.get('departureDate2')
        originLocationCode = cleaned_data.get('originLocationCode')
        destinationLocationCode = cleaned_data.get('destinationLocationCode')
        cabinType = cleaned_data.get('cabinType')
        numAdults = cleaned_data.get('numAdults')
        numChildren = cleaned_data.get('numChildren')

        # Check that departure date is not in the past
        if departureDate1 and departureDate1 < datetime.date.today():
            self.add_error('departureDate1', 'Departure date cannot be in the past.')

        # Check that return date is not before the departure date
        if departureDate2 and departureDate1 and departureDate2 < departureDate1:
            self.add_error('departureDate2', 'Return date cannot be before the departure date.')

        # Check that origin and destination are not the same
        if originLocationCode and destinationLocationCode and originLocationCode == destinationLocationCode:
            self.add_error('destinationLocationCode', 'You cannot select the same airport for departure and arrival.')

        # Check cabin type
        if cabinType not in ['ECONOMY', 'BUSINESS', 'FIRST']:
            self.add_error('cabinType', 'Invalid cabin type selected.')


        # Validate number of passengers
        if numAdults and numAdults > 9:
            self.add_error('numAdults', 'You cannot book for more than 9 adults at once.')
        if numChildren and numChildren > 9:
            self.add_error('numChildren', 'You cannot book for more than 9 children at once.')

        return cleaned_data

def get_iata_code(user_input):
    try:
        airport = Airport.objects.get(name__iexact=user_input)
        return airport.iata_code
    except Airport.DoesNotExist:
        try:
            airport = Airport.objects.get(iata_code__iexact=user_input)
            return airport.iata_code
        except Airport.DoesNotExist:
            return user_input

def autocomplete(request):
    q = request.GET.get('q', '')
    airports = Airport.objects.filter(Q(name__icontains=q) | Q(iata_code__icontains=q))
    results = [airport.name for airport in airports]
    return JsonResponse(results, safe=False)

#

def search_form(request):
    if request.method == "POST":
        return handle_search_form_submission(request)
        
    today = datetime.date.today()
    context = {
        'today': today.isoformat(),
        'form': SearchForm(),
    }
    return render(request, 'Bingo/search_form.html', context)


def handle_search_form_submission(request):
    form = SearchForm(request.POST)

    logger.info(f"Form data: {request.POST}")

    if form.is_valid():
    
        logger.info("Form is valid.")
        num_adults = form.cleaned_data['numAdults']
        num_children = form.cleaned_data['numChildren']
        cabin_type = form.cleaned_data['cabinType']
        currency_code = form.cleaned_data['currencyCode']
        origin_code = get_iata_code(form.cleaned_data['originLocationCode'])
        destination_code = get_iata_code(form.cleaned_data['destinationLocationCode'])
        departure_date1 = form.cleaned_data['departureDate1']
        flight_type = form.cleaned_data['flightType']
        departure_date2 = form.cleaned_data['departureDate2'] if flight_type == 'Return' else None
        
        travelers = [{"id": str(i+1), "travelerType": "ADULT"} for i in range(num_adults)]
        if num_children > 0:
            travelers.extend([{"id": str(i+1+num_adults), "travelerType": "CHILD"} for i in range(num_children)])

        data = {
            "currencyCode": currency_code,
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": origin_code,
                    "destinationLocationCode": destination_code,
                    "departureDateTimeRange": {
                        "date": departure_date1.isoformat()
                    }
                }
            ],
            "travelers": travelers,
            "sources": ["GDS"],
            "searchCriteria": {
                "flightFilters": {
                    "cabinRestrictions": [
                        {
                            "cabin": cabin_type,
                            "coverage": "MOST_SEGMENTS",
                            "originDestinationIds": [
                                "1"
                            ]
                        }
                    ]
                }
            }
        }

        if flight_type == 'Return':
            data['originDestinations'].append(
                {
                    "id": "2",
                    "originLocationCode": destination_code,
                    "destinationLocationCode": origin_code,
                    "departureDateTimeRange": {
                        "date": departure_date2.isoformat()
                    }
                }
            )
            
        try:
            response_data = get_ticket_data(data)
            modified_response = {
                "meta": {
                    "count": response_data["meta"]["count"]
                },
                "data": []
            }

            for flight_offer in response_data["data"]:
                modified_flight_offer = {
                    "type": flight_offer["type"],
                    "id": flight_offer["id"],
                    "lastTicketingDate": flight_offer["lastTicketingDate"],
                    "lastTicketingDateTime": flight_offer["lastTicketingDateTime"],
                    "numberOfBookableSeats": flight_offer["numberOfBookableSeats"],
                    "itineraries": [],
                    "price": {
                        "currency": currency_code,
                        "total": flight_offer["price"]["total"],
                        "grandTotal": flight_offer["price"]["grandTotal"]
                    },
                    "travelerPricings": []
                }

                for itinerary in flight_offer["itineraries"]:
                    modified_itinerary = {
                        "duration": itinerary["duration"],
                        "segments": []
                    }

                    for segment in itinerary["segments"]:
                        modified_segment = {
                            "departure": segment["departure"],
                            "arrival": segment["arrival"],
                            "carrierCode": segment["carrierCode"],
                            "number": segment["number"],
                            "duration": segment["duration"]
                        }

                        modified_itinerary["segments"].append(modified_segment)

                    modified_flight_offer["itineraries"].append(modified_itinerary)

                for traveler_pricing in flight_offer["travelerPricings"]:
                    modified_traveler_pricing = {
                        "travelerId": traveler_pricing["travelerId"],
                        "fareOption": traveler_pricing["fareOption"],
                        "travelerType": traveler_pricing["travelerType"],
                        "price": {
                            "currency": currency_code,
                            "total": traveler_pricing["price"]["total"]
                        },
                        "fareDetailsBySegment": []
                    }

                    for fare_detail in traveler_pricing["fareDetailsBySegment"]:
                        modified_fare_detail = {
                            "cabin": fare_detail["cabin"]
                        }

                        modified_traveler_pricing["fareDetailsBySegment"].append(modified_fare_detail)

                    modified_flight_offer["travelerPricings"].append(modified_traveler_pricing)

                modified_response["data"].append(modified_flight_offer)

            # return JsonResponse(modified_response, safe=False) # this is the original line used to Json response TEMP TEMP TEMP 
            return render(request, 'Bingo/search_results.html', {'data': modified_response['data']})
            # return render(request, 'Bingo/search_results.html', {'flights': modified_response['data']})


        except Exception as e:
            traceback.print_exc() # needed if you want to print the the trackback information on an exception
            logger.error(f'Error processing request: {e}')
            return HttpResponseBadRequest('Error processing request')
    else:  
        logger.info("Form is not valid.")
        logger.info(f"Form errors: {form.errors}")

    return HttpResponseBadRequest('Invalid form submission')




@csrf_exempt
def flight_search(request):
    if request.method == "POST":
        try:
            json_data = json.loads(request.body)
            ret_data = get_ticket_data(json_data)
            return JsonResponse(ret_data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)



