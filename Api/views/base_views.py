from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import FlightsSerializer, AirlineCompaniesSerializer, CountriesSerializer
from Bingo.facades.facade_base import FacadeBase
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)



@csrf_exempt
@api_view(['GET'])
def get_all_flights_api(request):

    print(request.user, request.user.is_authenticated)
    
    if request.method == "GET":
        try:
            facade = FacadeBase(request)
            flights = facade.get_all_flights()
            serializer = FlightsSerializer(flights, many=True)
            logger.info("Successfully fetched all flights.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching all flights: {str(e)}")
            return Response({"error": "Error fetching flights."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def get_flight_by_id_api(request, id):
    if request.method == "GET":
        facade = FacadeBase(request)
        flight = facade.get_flight_by_id(id)
        if flight:
            serializer = FlightsSerializer(flight)
            logger.info(f"Successfully fetched flight with id: {id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Flight with id {id} not found.")
        return Response({"error": "Flight not found."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
def get_all_airlines_api(request):
    if request.method == "GET":
        try:
            facade = FacadeBase(request)
            airlines = facade.get_all_airlines()
            serializer = AirlineCompaniesSerializer(airlines, many=True)
            logger.info("Successfully fetched all airlines.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching all airlines: {str(e)}")
            return Response({"error": "Error fetching airlines."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def get_airline_by_id_api(request, iata_code):
    if request.method == "GET":
        facade = FacadeBase(request)
        airline = facade.get_airline_by_id(iata_code)
        if airline:
            serializer = AirlineCompaniesSerializer(airline)
            logger.info(f"Successfully fetched airline with IATA code: {iata_code}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Airline with IATA code {iata_code} not found.")
        return Response({"error": "Airline not found."}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET'])
def get_all_countries_api(request):
    if request.method == "GET":
        try:
            facade = FacadeBase(request)
            countries = facade.get_all_countries()
            serializer = CountriesSerializer(countries, many=True)
            logger.info("Successfully fetched all countries.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching all countries: {str(e)}")
            return Response({"error": "Error fetching countries."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['GET'])
def get_country_by_id_api(request, country_code):
    if not (len(country_code) == 2 and country_code.isalpha()):
        return Response({"error": "Invalid country code format. It should be a 2-character alphabetic code."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        facade = FacadeBase(request)
        country = facade.get_country_by_id(country_code)
        if country:
            serializer = CountriesSerializer(country)
            logger.info(f"Successfully fetched country with code: {country_code}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        logger.warning(f"Country with code {country_code} not found.")
        return Response({"error": "Country not found."}, status=status.HTTP_404_NOT_FOUND)
