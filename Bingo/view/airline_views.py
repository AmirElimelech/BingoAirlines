from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from ..models import Airline_Companies
import json
from ..decorators import login_required

@login_required
@require_http_methods(["GET"])
def list_airlines(request):
    airlines = Airline_Companies.objects.all().values()
    return JsonResponse(list(airlines), safe=False)

@login_required
@require_http_methods(["GET"])
def get_airline(request, iata_code):
    try:
        airline = Airline_Companies.objects.get(iata_code=iata_code)
        return JsonResponse({
            'iata_code': airline.iata_code,
            'name': airline.name,
            'country_id': airline.country_id_id,
            'user_id': airline.user_id_id,
            'logo': airline.logo.url if airline.logo else None
        })
    except ObjectDoesNotExist:
        return HttpResponse('Airline not found', status=404)

@login_required
@require_http_methods(["POST"])
def add_airline(request):
    data = json.loads(request.body)
    try:
        airline = Airline_Companies.objects.create(**data)
        return JsonResponse({'message': 'Airline created successfully!', 'iata_code': airline.iata_code}, status=201)
    except Exception as e:
        return HttpResponse(str(e), status=400)

@login_required
@require_http_methods(["PUT"])
def update_airline(request, iata_code):
    data = json.loads(request.body)
    try:
        airline = Airline_Companies.objects.get(iata_code=iata_code)
        for key, value in data.items():
            setattr(airline, key, value)
        airline.save()
        return JsonResponse({'message': 'Airline updated successfully!'})
    except ObjectDoesNotExist:
        return HttpResponse('Airline not found', status=404)
    except Exception as e:
        return HttpResponse(str(e), status=400)

@login_required
@require_http_methods(["DELETE"])
def delete_airline(request, iata_code):
    try:
        airline = Airline_Companies.objects.get(iata_code=iata_code)
        airline.delete()
        return JsonResponse({'message': 'Airline deleted successfully!'})
    except ObjectDoesNotExist:
        return HttpResponse('Airline not found', status=404)
