import json
import logging
import datetime
import traceback

from django import forms
from django.db.models import Q
from django.shortcuts import render 
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest



from ..models import Airport , DAL
from ..utils.amadeus import get_ticket_data





# logger 
logger = logging.getLogger(__name__)



class SearchForm(forms.Form):
    logging.info("Starting the clean method of SearchForm.")
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
        currencyCode = cleaned_data.get('currencyCode')


        # Check that all fields are filled

        # Check that departure date is not in the past
        if departureDate1 and departureDate1 < datetime.date.today():
            logging.error("Error: Departure date is in the past.")
            self.add_error('departureDate1', 'Departure date cannot be in the past.')

        # Check that return date is not before the departure date
        if departureDate2 and departureDate1 and departureDate2 < departureDate1:
            logging.error("Error: Return date is before the departure date.")
            self.add_error('departureDate2', 'Return date cannot be before the departure date.')

        # Check that origin and destination are not the same
        if originLocationCode and destinationLocationCode and originLocationCode == destinationLocationCode:
            logging.error("Error: Origin and destination are the same.")
            self.add_error('destinationLocationCode', 'You cannot select the same airport for departure and arrival.')

        # Check cabin type
        if cabinType not in ['ECONOMY', 'BUSINESS', 'FIRST']:
            logging.error("Error: Invalid cabin type selected.")
            self.add_error('cabinType', 'Invalid cabin type selected.')


        # Validate number of passengers
        if numAdults and numAdults > 9:
            logging.error("Error: Too many adults selected.")
            self.add_error('numAdults', 'You cannot book for more than 9 adults at once.')
        if numChildren and numChildren > 9:
            logging.error("Error: Too many children selected.")
            self.add_error('numChildren', 'You cannot book for more than 9 children at once.')


        # Validate currency code
        if currencyCode not in ['USD', 'EUR', 'GBP', 'ILS']:
            logging.error("Error: Invalid currency code selected.")
            self.add_error('currencyCode', 'Invalid currency code selected.')


        return cleaned_data




def get_iata_code(user_input):

    """
    Get the IATA code of an airport from the database, given a user input.
    """

    try:
        airport = Airport.objects.get(name__iexact=user_input)
        return airport.iata_code
    except Airport.DoesNotExist:
        try:
            airport = Airport.objects.get(iata_code__iexact=user_input)
            return airport.iata_code
        except Airport.DoesNotExist:
            logging.warning(f"Could not find airport with name or IATA code: {user_input}")
            return user_input







def autocomplete(request):
    """
    Return a list of airports matching the user's query. this function is used in the search form to 
    autocomplete the user's input ( the user can type the airport name or the IATA code or part of it ) 
    and the function will return a list of airports matching the user's input.
    """

    q = request.GET.get('q', '')
    
    # Create the DAL instance and filter the airports
    dal_instance = DAL()
    query_params = Q(name__icontains=q) | Q(iata_code__icontains=q)
    airports = dal_instance.filter_by_query(Airport, query=query_params)

    results = [airport.name for airport in airports] if airports else []
    logging.info(f"Found {len(results)} airports matching query: {q}")
    return JsonResponse(results, safe=False)




def search_form(request):

    """
    Render the search form.
    """

    try:
        if request.method == "POST":
            return handle_search_form_submission(request)

        today = datetime.date.today()
        context = {
            'today': today.isoformat(),
            'form': SearchForm(),
        }
        logging.info("Rendering search form.")
        return render(request, 'Bingo/search_form.html', context)

    except Exception as e:
        logger.error(f"Error while rendering search form: {str(e)}")
        # Optionally, return a response indicating an error occurred, for example:
        # return render(request, 'error_page.html', {'error_message': 'Error rendering search form.'}) << i need to finish this as well ! 




def handle_search_form_submission(request):

    """
    Handle the form submission for searching flight tickets.

    This function processes the submitted search form data to look for available flights.
    It validates the form data, constructs the appropriate search query, and then fetches 
    flight offers based on the criteria provided in the form. The results are then 
    transformed into a more concise format and rendered as needed .

    If the form is not valid, it returns an error. If there's an exception during the 
    process of fetching or handling the flight data, it logs the error and returns an 
    appropriate error message.


    """

    try:
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

                logging.info("Rendering search results...")
                return render(request, 'Bingo/search_results.html', {'data': modified_response['data']})

            except Exception as e:
                traceback.print_exc()
                logger.error(f'Error processing request: {e}')
                return HttpResponseBadRequest('Error processing request')

        else:
            logger.warning("Form is not valid.")
            logger.warning(f"Form errors: {form.errors}")
            return HttpResponseBadRequest('Invalid form submission')

    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)}")
        return HttpResponseBadRequest('An unexpected error occurred')



# from django.http import JsonResponse, HttpResponseBadRequest

# def handle_search_form_submission(request):
#     """
#     Handle the form submission for searching flight tickets.

#     This function processes the submitted search form data to look for available flights.
#     It validates the form data, constructs the appropriate search query, and then fetches 
#     flight offers based on the criteria provided in the form. The results are then 
#     transformed into a more concise format and rendered as a JSON response.

#     If the form is not valid, it returns an error. If there's an exception during the 
#     process of fetching or handling the flight data, it logs the error and returns an 
#     appropriate error message.
#     """

#     try:
#         form = SearchForm(request.POST)

#         logger.info(f"Form data: {request.POST}")

#         if form.is_valid():
#             logger.info("Form is valid.")
#             num_adults = form.cleaned_data['numAdults']
#             num_children = form.cleaned_data['numChildren']
#             cabin_type = form.cleaned_data['cabinType']
#             currency_code = form.cleaned_data['currencyCode']
#             origin_code = get_iata_code(form.cleaned_data['originLocationCode'])
#             destination_code = get_iata_code(form.cleaned_data['destinationLocationCode'])
#             departure_date1 = form.cleaned_data['departureDate1']
#             flight_type = form.cleaned_data['flightType']
#             departure_date2 = form.cleaned_data['departureDate2'] if flight_type == 'Return' else None

#             travelers = [{"id": str(i+1), "travelerType": "ADULT"} for i in range(num_adults)]
#             if num_children > 0:
#                 travelers.extend([{"id": str(i+1+num_adults), "travelerType": "CHILD"} for i in range(num_children)])

#             data = {
#                 "currencyCode": currency_code,
#                 "originDestinations": [
#                     {
#                         "id": "1",
#                         "originLocationCode": origin_code,
#                         "destinationLocationCode": destination_code,
#                         "departureDateTimeRange": {
#                             "date": departure_date1.isoformat()
#                         }
#                     }
#                 ],
#                 "travelers": travelers,
#                 "sources": ["GDS"],
#                 "searchCriteria": {
#                     "flightFilters": {
#                         "cabinRestrictions": [
#                             {
#                                 "cabin": cabin_type,
#                                 "coverage": "MOST_SEGMENTS",
#                                 "originDestinationIds": [
#                                     "1"
#                                 ]
#                             }
#                         ]
#                     }
#                 }
#             }

#             if flight_type == 'Return':
#                 data['originDestinations'].append(
#                     {
#                         "id": "2",
#                         "originLocationCode": destination_code,
#                         "destinationLocationCode": origin_code,
#                         "departureDateTimeRange": {
#                             "date": departure_date2.isoformat()
#                         }
#                     }
#                 )

#             try:
#                 response_data = get_ticket_data(data)
#                 modified_response = {
#                     "meta": {
#                         "count": response_data["meta"]["count"]
#                     },
#                     "data": []
#                 }

#                 for flight_offer in response_data["data"]:
#                     modified_flight_offer = {
#                         "type": flight_offer["type"],
#                         "id": flight_offer["id"],
#                         "lastTicketingDate": flight_offer["lastTicketingDate"],
#                         "lastTicketingDateTime": flight_offer["lastTicketingDateTime"],
#                         "numberOfBookableSeats": flight_offer["numberOfBookableSeats"],
#                         "itineraries": [],
#                         "price": {
#                             "currency": currency_code,
#                             "total": flight_offer["price"]["total"],
#                             "grandTotal": flight_offer["price"]["grandTotal"]
#                         },
#                         "travelerPricings": []
#                     }

#                     for itinerary in flight_offer["itineraries"]:
#                         modified_itinerary = {
#                             "duration": itinerary["duration"],
#                             "segments": []
#                         }

#                         for segment in itinerary["segments"]:
#                             modified_segment = {
#                                 "departure": segment["departure"],
#                                 "arrival": segment["arrival"],
#                                 "carrierCode": segment["carrierCode"],
#                                 "number": segment["number"],
#                                 "duration": segment["duration"]
#                             }

#                             modified_itinerary["segments"].append(modified_segment)

#                         modified_flight_offer["itineraries"].append(modified_itinerary)

#                     for traveler_pricing in flight_offer["travelerPricings"]:
#                         modified_traveler_pricing = {
#                             "travelerId": traveler_pricing["travelerId"],
#                             "fareOption": traveler_pricing["fareOption"],
#                             "travelerType": traveler_pricing["travelerType"],
#                             "price": {
#                                 "currency": currency_code,
#                                 "total": traveler_pricing["price"]["total"]
#                             },
#                             "fareDetailsBySegment": []
#                         }

#                         for fare_detail in traveler_pricing["fareDetailsBySegment"]:
#                             modified_fare_detail = {
#                                 "cabin": fare_detail["cabin"]
#                             }

#                             modified_traveler_pricing["fareDetailsBySegment"].append(modified_fare_detail)

#                         modified_flight_offer["travelerPricings"].append(modified_traveler_pricing)

#                     modified_response["data"].append(modified_flight_offer)

#                 # Create a dictionary containing the payload and the results
#                 json_response = {
#                     "payload": data,
#                     "results": modified_response
#                 }

#                 # Return the dictionary as a JSON response
#                 return JsonResponse(json_response)

#             except Exception as e:
#                 traceback.print_exc()
#                 logger.error(f'Error processing request: {e}')
#                 return HttpResponseBadRequest('Error processing request')

#         else:
#             logger.warning("Form is not valid.")
#             logger.warning(f"Form errors: {form.errors}")
#             return HttpResponseBadRequest('Invalid form submission')

#     except Exception as e:
#         logger.error(f"Unexpected error occurred: {str(e)}")
#         return HttpResponseBadRequest('An unexpected error occurred')




