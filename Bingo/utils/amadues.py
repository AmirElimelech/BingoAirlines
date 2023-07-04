import requests
import os

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