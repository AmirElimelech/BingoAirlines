from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from ..models import Administrators
import json
from ..decorators import login_required

@login_required
@require_http_methods(["GET"])
def list_administrators(request):
    admins = Administrators.objects.all().values()
    return JsonResponse(list(admins), safe=False)

@login_required
@require_http_methods(["GET"])
def get_administrator(request, admin_id):
    try:
        admin = Administrators.objects.get(id=admin_id)
        return JsonResponse({
            'id': admin.id,
            'first_name': admin.first_name,
            'last_name': admin.last_name,
            'user_id': admin.user_id_id
        })
    except ObjectDoesNotExist:
        return HttpResponse('Administrator not found', status=404)

@login_required
@require_http_methods(["POST"])
def add_administrator(request):
    data = json.loads(request.body)
    try:
        admin = Administrators.objects.create(**data)
        return JsonResponse({'message': 'Administrator created successfully!', 'id': admin.id}, status=201)
    except Exception as e:
        return HttpResponse(str(e), status=400)

@login_required
@require_http_methods(["PUT"])
def update_administrator(request, admin_id):
    data = json.loads(request.body)
    try:
        admin = Administrators.objects.get(id=admin_id)
        for key, value in data.items():
            setattr(admin, key, value)
        admin.save()
        return JsonResponse({'message': 'Administrator updated successfully!'})
    except ObjectDoesNotExist:
        return HttpResponse('Administrator not found', status=404)
    except Exception as e:
        return HttpResponse(str(e), status=400)

@login_required
@require_http_methods(["DELETE"])
def delete_administrator(request, admin_id):
    try:
        admin = Administrators.objects.get(id=admin_id)
        admin.delete()
        return JsonResponse({'message': 'Administrator deleted successfully!'})
    except ObjectDoesNotExist:
        return HttpResponse('Administrator not found', status=404)
