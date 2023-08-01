import requests
import os
import json


def get_token():
    url = "https://api.amadeus.com/v1/security/oauth2/token"
    # payload = 'grant_type=client_credentials&client_id=7IgQrqy0G2E0lcouQ7B3Dlo3bR43pUKi&client_secret=ZeW3niQftvla34pB' this is the old not so working token that got hacked 
    payload = 'grant_type=client_credentials&client_id=OEAF6GngPrGt0kXZklcxsviCcYAWo5TB&client_secret=9VF9tuFtnHeVbjkC' # this is the new token that works
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