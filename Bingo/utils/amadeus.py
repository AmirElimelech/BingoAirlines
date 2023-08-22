import requests , os , json , logging


logger = logging.getLogger(__name__)



def get_token():
    """
    Fetch and set the Amadeus API token.

    This function sends a request to the Amadeus API to obtain an access token. 
    Once obtained, the token is set as an environment variable and also returned.

    Returns:
    - str: The obtained API token.
    """

    try:
        url = "https://api.amadeus.com/v1/security/oauth2/token"
        # Using the new token
        payload = 'grant_type=client_credentials&client_id=OEAF6GngPrGt0kXZklcxsviCcYAWo5TB&client_secret=9VF9tuFtnHeVbjkC'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        token = response.json()['access_token']
        os.environ["amadeus-api-token"] = token
        return token
    except Exception as e:
        logger.error(f"Failed to fetch Amadeus API token. Error: {e}")
        raise  # Re-raise the exception to handle it further up in the call stack

def get_ticket_data(data):
    """
    Fetch flight ticket data from Amadeus API.

    This function sends a POST request to the Amadeus API with provided search criteria 
    to fetch flight offers. The function first ensures a valid API token is obtained
    and then sends the request.

    Parameters:
    - data (dict): A dictionary containing flight search criteria.

    Returns:
    - dict: A dictionary containing flight offer data.
    """

    try:
        get_token()  # Ensure we have a valid token
        url = "https://api.amadeus.com/v2/shopping/flight-offers"
        payload = json.dumps(data)
        headers = {
            'Authorization': f'Bearer {os.environ["amadeus-api-token"]}',
            'Content-Type': 'application/json'
        }


        logger.info("Fetching flight data from Amadeus API.")
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        logger.error(f"Failed to fetch ticket data from Amadeus API. Error: {e}")
        raise  # Re-raise the exception to handle it further up in the call stack
