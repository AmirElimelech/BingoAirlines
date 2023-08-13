import urllib.request
from django.core.files import File
import logging
from tempfile import NamedTemporaryFile
import os
from django.conf import settings



logger = logging.getLogger(__name__)



def download_airline_logo(iata_code):
    from Bingo.models import Airline_Companies
    logger.info(f"Download function called for iata_code: {iata_code}")
    
    airline = Airline_Companies.objects.get(iata_code=iata_code)

    # Attempt to download the logo
    url = f'https://content.r9cdn.net/rimg/provider-logos/airlines/v/{iata_code}.png?crop=false&width=100&height=100'
    logging.info(f"Attempting to download logo from URL: {url}")
    try:
        response = urllib.request.urlopen(url)
        if response.status == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(response.read())
            img_temp.flush()
            filename = f'{iata_code}.png'
            airline.logo.save(filename, File(img_temp), save=True)
            logging.info(f"Downloaded and saved logo for {iata_code} from {url}")
    except Exception as e:
        logging.info(f"Error when trying to download logo from {url}: {e}")
        airline.logo.name = 'airline_logos/airplanelogo.png'  # Point to the existing default logo file
        airline.save(update_fields=['logo'])  # Save the updated logo path without modifying the file



