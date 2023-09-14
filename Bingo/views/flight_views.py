import json
import logging
import traceback
from django.db.models import Q
from ..forms import SearchForm
from ..models import Airport , DAL
from ..utils.amadeus import get_ticket_data
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest




# logger 
logger = logging.getLogger(__name__)



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





@csrf_exempt
@api_view(['GET'])
def autocomplete(request):
    """
    Return a list of airports matching the user's query. This function is used in the search form to 
    autocomplete the user's input (the user can type the airport name or the IATA code or part of it) 
    and the function will return a list of airports matching the user's input.
    """
    q = request.GET.get('q', '')
    
    # Create the DAL instance and filter the airports
    dal_instance = DAL()
    query_params = Q(name__icontains=q) | Q(iata_code__iexact=q)  # Adjusted the query for iata_code
    airports = dal_instance.filter_by_query(Airport, query=query_params)

    # Instead of returning just names, return a list of dictionaries with both name and IATA code
    results = [{'name': airport.name, 'iata_code': airport.iata_code} for airport in airports] if airports else []
    logging.info(f"Found {len(results)} airports matching query: {q}")
    return JsonResponse(results, safe=False)



@csrf_exempt
def handle_search_form_submission(request):
    """
    Handle the form submission for searching flight tickets.

    This function processes the submitted search form data to look for available flights.
    It validates the form data, constructs the appropriate search query, and then fetches 
    flight offers based on the criteria provided in the form. The results are then 
    transformed into a more concise format and rendered as a JSON response.

    If the form is not valid, it returns an error. If there's an exception during the 
    process of fetching or handling the flight data, it logs the error and returns an 
    appropriate error message.
    """

    try:
        
        data = json.loads(request.body)
        form = SearchForm(data)

        logger.info(f"Form data: {request.POST}")
        logger.info(f"Form data: {data}")

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

                # Create a dictionary containing the payload and the results
                json_response = {
                    "payload": data,
                    "results": modified_response
                }

                # Return the dictionary as a JSON response
                return JsonResponse(json_response)

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




