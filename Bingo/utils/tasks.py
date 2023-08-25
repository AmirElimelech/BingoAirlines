
import logging
import urllib.request
from django.core.files import File
from tempfile import NamedTemporaryFile




logger = logging.getLogger(__name__)






def download_airline_logo(iata_code):

    """
    Download and save the logo for a given airline specified by its IATA code.
    
    The function tries to fetch the airline logo from a specific URL. If the download is 
    successful, it saves the logo associated with the airline's database record. If there's 
    an error during the download, the logo is set to a default image.

    according to django method of saving if the iata.png exists it will be added with same name beginning of the IATA code
    and the rest will be filled with random characters to avoid overwriting the existing logo .
    
    Parameters:
    - iata_code (str): The IATA code of the airline.
    """

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



