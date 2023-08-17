# from django.http import JsonResponse
# from ..facades.facade_base import FacadeBase

# def get_all_flights_view(request):
#     facade = FacadeBase(request)
#     flights = facade.get_all_flights()
#     # Assuming flights is a QuerySet, converting it to a list of dictionaries for JSON serialization
#     return JsonResponse({'flights': list(flights.values())}, safe=False)

# def get_flight_by_id_view(request, flight_id):
#     facade = FacadeBase(request)
#     flight = facade.get_flight_by_id(flight_id)
#     return JsonResponse({'flight': flight})

# def get_flights_by_parameters_view(request):
#     origin_country_id = request.GET.get('origin_country_id')
#     destination_country_id = request.GET.get('destination_country_id')
#     date = request.GET.get('date')
#     facade = FacadeBase(request)
#     flights = facade.get_flights_by_parameters(origin_country_id, destination_country_id, date)
#     return JsonResponse({'flights': list(flights.values())}, safe=False)

# def get_all_airlines_view(request):
#     facade = FacadeBase(request)
#     airlines = facade.get_all_airlines()
#     return JsonResponse({'airlines': list(airlines.values())}, safe=False)

# def get_airline_by_id_view(request, airline_id):
#     facade = FacadeBase(request)
#     airline = facade.get_airline_by_id(airline_id)
#     return JsonResponse({'airline': airline})

# def get_all_countries_view(request):
#     facade = FacadeBase(request)
#     countries = facade.get_all_countries()
#     return JsonResponse({'countries': list(countries.values())}, safe=False)

# def get_country_by_id_view(request, country_id):
#     facade = FacadeBase(request)
#     country = facade.get_country_by_id(country_id)
#     return JsonResponse({'country': country})




from django.http import JsonResponse
from ..models import DAL, Flights, Countries, Airline_Companies
import logging
from ..serializers import FlightsSerializer, CountriesSerializer, AirlineCompaniesSerializer



from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

class BaseViews():

    DAL_instance = DAL()


    @api_view(['GET'])
    def get_all_flights_view(self, request):
        flights = self.DAL_instance.get_all(Flights)
        serialized_flights = FlightsSerializer(flights, many=True)
        logger.info("Retrieved all flights.")
        return Response(serialized_flights.data, safe=False)

    def get_flight_by_id_view(self, request, flight_id):
        flight = self.DAL.get_by_id(Flights, flight_id)
        if flight:
            serialized_flight = FlightsSerializer(flight)
            logger.info(f"Retrieved flight with ID {flight_id}.")
            return JsonResponse(serialized_flight.data)
        else:
            logger.error(f"Flight with ID {flight_id} not found.")
            return JsonResponse({"error": "Flight not found."}, status=404)

    def get_flights_by_parameters_view(self, request, origin_country_id, destination_country_id, date):
        flights = self.DAL.get_flights_by_parameters(origin_country_id, destination_country_id, date)
        serialized_flights = FlightsSerializer(flights, many=True)
        logger.info(f"Retrieved flights based on parameters.")
        return JsonResponse(serialized_flights.data, safe=False)

    def get_all_airlines_view(self, request):
        airlines = self.DAL.get_all(Airline_Companies)
        serialized_airlines = AirlineCompaniesSerializer(airlines, many=True)
        logger.info("Retrieved all airline companies.")
        return JsonResponse(serialized_airlines.data, safe=False)

    def get_airline_by_id_view(self, request, airline_id):
        airline = self.DAL.get_by_id(Airline_Companies, airline_id)
        if airline:
            serialized_airline = AirlineCompaniesSerializer(airline)
            logger.info(f"Retrieved airline with ID {airline_id}.")
            return JsonResponse(serialized_airline.data)
        else:
            logger.error(f"Airline with ID {airline_id} not found.")
            return JsonResponse({"error": "Airline not found."}, status=404)

    def get_all_countries_view(self, request):
        countries = self.DAL.get_all(Countries)
        serialized_countries = CountriesSerializer(countries, many=True)
        logger.info("Retrieved all countries.")
        return JsonResponse(serialized_countries.data, safe=False)

    def get_country_by_id_view(self, request, country_id):
        country = self.DAL.get_by_id(Countries, country_id)
        if country:
            serialized_country = CountriesSerializer(country)
            logger.info(f"Retrieved country with ID {country_id}.")
            return JsonResponse(serialized_country.data)
        else:
            logger.error(f"Country with ID {country_id} not found.")
            return JsonResponse({"error": "Country not found."}, status=404)
