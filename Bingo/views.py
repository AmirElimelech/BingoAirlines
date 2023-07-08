from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from .utils.amadeus import get_ticket_data
import json
from django.views.decorators.csrf import csrf_exempt
import datetime


# 

# def search_form(request):
#     if request.method == "POST":
#         data = {
#             "currencyCode": request.POST.get('currencyCode'),
#             "originDestinations": [
#                 {
#                     "id": "1",
#                     "originLocationCode": request.POST.get('originLocationCode1'),
#                     "destinationLocationCode": request.POST.get('destinationLocationCode1'),
#                     "departureDateTimeRange": {
#                         "date": request.POST.get('departureDate1')
#                     }
#                 },
#                 {
#                     "id": "2",
#                     "originLocationCode": request.POST.get('originLocationCode2'),
#                     "destinationLocationCode": request.POST.get('destinationLocationCode2'),
#                     "departureDateTimeRange": {
#                         "date": request.POST.get('departureDate2')
#                     }
#                 }
#             ],
#             # Add more fields as required
#         }

#         response_data = get_ticket_data(data)
#         return JsonResponse(response_data, safe=False)

#     return render(request, 'Bingo/search_form.html')

def search_form(request):
    if request.method == "POST":
        num_adults = int(request.POST.get('numAdults', 1))
        num_children = int(request.POST.get('numChildren', 0))
        travelers = [{"id": str(i+1), "travelerType": "ADULT"} for i in range(num_adults)]
        if num_children > 0:
            travelers.extend([{"id": str(i+1+num_adults), "travelerType": "CHILD"} for i in range(num_children)])

        data = {
            "currencyCode": request.POST.get('currencyCode', 'USD'),
            "originDestinations": [
                {
                    "id": "1",
                    "originLocationCode": request.POST.get('originLocationCode'),
                    "destinationLocationCode": request.POST.get('destinationLocationCode'),
                    "departureDateTimeRange": {
                        "date": request.POST.get('departureDate1')
                    }
                }
            ],
            "travelers": travelers,
            "sources": ["GDS"],
        }

        if request.POST.get('flightType') == 'Return':
            data['originDestinations'].append(
                {
                    "id": "2",
                    "originLocationCode": request.POST.get('destinationLocationCode'),
                    "destinationLocationCode": request.POST.get('originLocationCode'),
                    "departureDateTimeRange": {
                        "date": request.POST.get('departureDate2')
                    }
                }
            )

        response_data = get_ticket_data(data)
        return JsonResponse(response_data, safe=False)

    today = datetime.date.today()
    context = {
        'today': today.isoformat(),
    }
    return render(request, 'Bingo/search_form.html', context)




@csrf_exempt
def flight_search(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        ret_data = get_ticket_data(json_data)
        return JsonResponse(ret_data,safe=False)
    

def home(request):
    return HttpResponse("Hello, world. You're at the Bingo Airlines home page hello hello.")


    
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