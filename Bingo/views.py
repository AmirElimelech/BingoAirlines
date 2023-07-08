# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from .utils.amadeus import get_ticket_data
# from .models import Airport
# import json
# import datetime
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q


# # def getIATACode(city_name):
# #     try:
# #         airport = Airport.objects.get(name__iexact=city_name)
# #         return airport.iata_code
# #     except Airport.DoesNotExist:
# #         return city_name  # return the original input if no airport is found
# def getIATACode(user_input):
#     try:
#         # try finding by name
#         airport = Airport.objects.get(name__iexact=user_input)
#         return airport.iata_code
#     except Airport.DoesNotExist:
#         try:
#             # if not found by name, try finding by iata_code
#             airport = Airport.objects.get(iata_code__iexact=user_input)
#             return airport.iata_code
#         except Airport.DoesNotExist:
#             # if not found either by name or by iata_code, return the original input
#             return user_input



# def autocomplete(request):
#     q = request.GET.get('q', '')
#     airports = Airport.objects.filter(Q(name__icontains=q) | Q(iata_code__icontains=q))
#     results = [airport.name for airport in airports]
#     return JsonResponse(results, safe=False)


# def search_form(request):
#     if request.method == "POST":
#         num_adults = int(request.POST.get('numAdults', 1))
#         num_children = int(request.POST.get('numChildren', 0))
#         travelers = [{"id": str(i+1), "travelerType": "ADULT"} for i in range(num_adults)]
#         if num_children > 0:
#             travelers.extend([{"id": str(i+1+num_adults), "travelerType": "CHILD"} for i in range(num_children)])

#         cabin_type = request.POST.get('cabinType', 'ECONOMY')

#         data = {
#             "currencyCode": request.POST.get('currencyCode', 'USD'),
#             "originDestinations": [
#                 {
#                     "id": "1",
#                     "originLocationCode": getIATACode(request.POST.get('originLocationCode')),
#                     "destinationLocationCode": getIATACode(request.POST.get('destinationLocationCode')),
#                     "departureDateTimeRange": {
#                         "date": request.POST.get('departureDate1')
#                     }
#                 }
#             ],
#             "travelers": travelers,
#             "sources": ["GDS"],
#             "searchCriteria": {
#                 # "maxFlightOffers": 10, #this number is the max number of results change it to 255 if your don't want restrictions on the number of results
#                 "flightFilters": {
#                     "cabinRestrictions": [
#                         {
#                             "cabin": cabin_type,
#                             "coverage": "MOST_SEGMENTS",
#                             "originDestinationIds": [
#                                 "1"
#                             ]
#                         }
#                     ]
#                 }
#             }
#         }

#         if request.POST.get('flightType') == 'Return':
#             data['originDestinations'].append(
#                 {
#                     "id": "2",
#                     "originLocationCode": getIATACode(request.POST.get('destinationLocationCode')),
#                     "destinationLocationCode": getIATACode(request.POST.get('originLocationCode')),
#                     "departureDateTimeRange": {
#                         "date": request.POST.get('departureDate2')
#                     }
#                 }
#             )

#         response_data = get_ticket_data(data)
#         return JsonResponse(response_data, safe=False)

#     today = datetime.date.today()
#     context = {
#         'today': today.isoformat(),
#     }
#     return render(request, 'Bingo/search_form.html', context)


# @csrf_exempt
# def flight_search(request):
#     if request.method == "POST":
#         json_data = json.loads(request.body)
#         ret_data = get_ticket_data(json_data)
#         return JsonResponse(ret_data, safe=False)


# def home(request):
#     return HttpResponse("Hello, world. You're at the Bingo Airlines home page hello hello.")

    
# def add_user_view(request):
#     user_role = user_roles_dal.get_by_id(1)
#     new_user = users_dal.add(
#         id="112233445",
#         username="testuser",
#         password="testpassword",
#         email="test@example.com",
#         user_role=user_role,
#     )


#     return HttpResponse(f"New user {new_user.username} created with ID {new_user.id}.")



# def show_users(request):
#     users = users_dal.get_all()
#     output = ', '.join([u.username for u in users])
#     return HttpResponse(output)


# def update_user(request,pk):
#     user = users_dal.get_by_id(pk)
#     user = users_dal.update(pk, username="newusername")
#     return HttpResponse(f"User {user.id} updated to {user.username}.")

# from django import forms
# from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
# from django.shortcuts import render
# from .utils.amadeus import get_ticket_data
# from .models import Airport
# import json
# import datetime
# from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q

# class SearchForm(forms.Form):
#     numAdults = forms.IntegerField(min_value=1, initial=1 , label='Adults')
#     numChildren = forms.IntegerField(min_value=0, initial=0 , label='Children')
#     cabinType = forms.ChoiceField(choices=[('ECONOMY', 'Economy'), ('BUSINESS', 'Business'), ('FIRST', 'First')] , label='Cabin Type')
#     currencyCode = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP'), ('ILS', 'ILS')] , label='Currency')
#     originLocationCode = forms.CharField(label='Flying From') 
#     destinationLocationCode = forms.CharField(label='Flying To')
#     departureDate1 = forms.DateField(label='Departure Date')
#     flightType = forms.ChoiceField(choices=[('OneWay', 'One Way'), ('Return', 'Return Flight')] , label='Flight Type')
#     departureDate2 = forms.DateField(required=False , label='Return Date')

# def get_iata_code(user_input):
#     try:
#         airport = Airport.objects.get(name__iexact=user_input)
#         return airport.iata_code
#     except Airport.DoesNotExist:
#         try:
#             airport = Airport.objects.get(iata_code__iexact=user_input)
#             return airport.iata_code
#         except Airport.DoesNotExist:
#             return user_input

# def autocomplete(request):
#     q = request.GET.get('q', '')
#     airports = Airport.objects.filter(Q(name__icontains=q) | Q(iata_code__icontains=q))
#     results = [airport.name for airport in airports]
#     return JsonResponse(results, safe=False)

# def search_form(request):
#     if request.method == "POST":
#         return handle_search_form_submission(request)
        
#     today = datetime.date.today()
#     context = {
#         'today': today.isoformat(),
#         'form': SearchForm(),
#     }
#     return render(request, 'Bingo/search_form.html', context)

# def handle_search_form_submission(request):
#     form = SearchForm(request.POST)

#     if form.is_valid():
#         num_adults = form.cleaned_data['numAdults']
#         num_children = form.cleaned_data['numChildren']
#         cabin_type = form.cleaned_data['cabinType']
#         currency_code = form.cleaned_data['currencyCode']
#         origin_code = get_iata_code(form.cleaned_data['originLocationCode'])
#         destination_code = get_iata_code(form.cleaned_data['destinationLocationCode'])
#         departure_date1 = form.cleaned_data['departureDate1']
#         flight_type = form.cleaned_data['flightType']
#         departure_date2 = form.cleaned_data['departureDate2'] if flight_type == 'Return' else None
        
#         travelers = [{"id": str(i+1), "travelerType": "ADULT"} for i in range(num_adults)]
#         if num_children > 0:
#             travelers.extend([{"id": str(i+1+num_adults), "travelerType": "CHILD"} for i in range(num_children)])

#         data = {
#             "currencyCode": currency_code,
#             "originDestinations": [
#                 {
#                     "id": "1",
#                     "originLocationCode": origin_code,
#                     "destinationLocationCode": destination_code,
#                     "departureDateTimeRange": {
#                         "date": departure_date1.isoformat()
#                     }
#                 }
#             ],
#             "travelers": travelers,
#             "sources": ["GDS"],
#             "searchCriteria": {
#                 "flightFilters": {
#                     "cabinRestrictions": [
#                         {
#                             "cabin": cabin_type,
#                             "coverage": "MOST_SEGMENTS",
#                             "originDestinationIds": [
#                                 "1"
#                             ]
#                         }
#                     ]
#                 }
#             }
#         }

#         if flight_type == 'Return':
#             data['originDestinations'].append(
#                 {
#                     "id": "2",
#                     "originLocationCode": destination_code,
#                     "destinationLocationCode": origin_code,
#                     "departureDateTimeRange": {
#                         "date": departure_date2.isoformat()
#                     }
#                 }
#             )
            
#         try:
#             response_data = get_ticket_data(data)
#             return JsonResponse(response_data, safe=False)
#         except Exception as e:
#             return HttpResponseBadRequest('Error processing request')

#     return HttpResponseBadRequest('Invalid form submission')

# @csrf_exempt
# def flight_search(request):
#     if request.method == "POST":
#         try:
#             json_data = json.loads(request.body)
#             ret_data = get_ticket_data(json_data)
#             return JsonResponse(ret_data, safe=False)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

# def home(request):
#     return HttpResponse("Hello, world. You're at the Bingo Airlines home page.")



from django import forms
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from .utils.amadeus import get_ticket_data
from .models import Airport
import json
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import ValidationError

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

        # Check that departure date is not in the past
        if departureDate1 and departureDate1 < datetime.date.today():
            self.add_error('departureDate1', 'Departure date cannot be in the past.')

        # Check that return date is not before the departure date
        if departureDate2 and departureDate1 and departureDate2 < departureDate1:
            self.add_error('departureDate2', 'Return date cannot be before the departure date.')

        # Check that origin and destination are not the same
        if originLocationCode and destinationLocationCode and originLocationCode == destinationLocationCode:
            self.add_error('destinationLocationCode', 'You cannot select the same airport for departure and arrival.')

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

    if form.is_valid():
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
            return JsonResponse(response_data, safe=False)
        except Exception as e:
            return HttpResponseBadRequest('Error processing request')

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

def home(request):
    return HttpResponse("Hello, world. You're at the Bingo Airlines home page.")
