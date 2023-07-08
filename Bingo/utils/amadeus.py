import requests
import os
import json


def get_token():
    url = "https://api.amadeus.com/v1/security/oauth2/token"
    payload = 'grant_type=client_credentials&client_id=7IgQrqy0G2E0lcouQ7B3Dlo3bR43pUKi&client_secret=ZeW3niQftvla34pB'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    token = response.json()['access_token']
    os.environ["amadeus-api-token"] = token
    return token
def get_ticket_data(data):
    get_token()
    url = "https://api.amadeus.com/v2/shopping/flight-offers"

    payload = json.dumps(data)
    headers = {
        'Authorization': f'Bearer {os.environ["amadeus-api-token"]}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()
# data = {
#         "currencyCode": "USD",
#         "originDestinations": [
#             {
#                 "id": "1",
#                 "originLocationCode": "TLV",
#                 "destinationLocationCode": "ATH",
#                 "departureDateTimeRange": {
#                     "date": "2023-07-26",
#                     "time": "10:00:00"
#                 }
#             },
#             {
#                 "id": "2",
#                 "originLocationCode": "ATH",
#                 "destinationLocationCode": "TLV",
#                 "departureDateTimeRange": {
#                     "date": "2023-07-29",
#                     "time": "10:00:00"
#                 }
#             }
#         ],
#         "travelers": [
#             {
#                 "id": "1",
#                 "travelerType": "ADULT"
#             }
#         ],
#         "sources": [
#             "GDS"
#         ],
#         "searchCriteria": {
#             "maxFlightOffers": 3,
#             "flightFilters": {
#                 "cabinRestrictions": [
#                     {
#                         "cabin": "ECONOMY",
#                         "coverage": "MOST_SEGMENTS",
#                         "originDestinationIds": [
#                             "1"
#                         ]
#                     }
#                 ],
#                 "ConnectionRestriction": [
#                     {
#                         "nonStopPreferred": True
#                     }
#                 ]
#             }
#         }
#     }
# data_ = get_ticket_data(data)
# print(data_)