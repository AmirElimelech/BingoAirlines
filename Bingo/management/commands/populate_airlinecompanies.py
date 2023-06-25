import pandas as pd
from django.core.management.base import BaseCommand
from django.core.files import File
from tempfile import NamedTemporaryFile
import requests
from Bingo.models import Users, Countries, Airline_Companies

class Command(BaseCommand):
    help = 'Loads airline companies from airlinecompaniespopulate.csv file into the database'

    def handle(self, *args, **options):
        # Read the country mapping from countries.csv
        country_df = pd.read_csv('Bingo/management/commands/countries.csv')
        country_mapping = {name: code for name, code in zip(country_df['Country name'], country_df['Country Code'])}

        df = pd.read_csv('Bingo/management/commands/airlinecompaniespopulate.csv', keep_default_na=False)

        for index, row in df.iterrows():
            iata_code = row['IATA']
            airline_name = row['Airline']
            country_name = row['Country']
            user_id = str(row['ID']).zfill(9)  # Pad the ID with leading zeros
            logo_url = row['Logo']

            # Check if airline_name is a valid string
            if isinstance(airline_name, str):
                # Get corresponding user for the airline
                try:
                    user = Users.objects.get(id=user_id)
                except Users.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"User not found for airline: {airline_name} (ID: {user_id})"))
                    continue

                # Get corresponding country for the airline
                country_code = None
                for key, value in country_mapping.items():
                    if key.startswith(country_name):
                        country_code = value
                        break

                if country_code is None:
                    self.stdout.write(self.style.WARNING(f"Country not found in mapping: {country_name}"))
                    continue

                try:
                    country = Countries.objects.get(country_code=country_code)
                except Countries.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Country not found in database: {country_code}"))
                    continue

                # Check if the airline with the same iata_code already exists
                if Airline_Companies.objects.filter(iata_code=iata_code).exists():
                    self.stdout.write(self.style.WARNING(f"Skipping duplicate entry: {airline_name} (IATA Code: {iata_code})"))
                    continue
                
                # Create a new airline company
                airline_company = Airline_Companies(iata_code=iata_code, name=airline_name, country_id=country, user_id=user)

                 # Save logo
                img_temp = NamedTemporaryFile(delete=True)
                response = requests.get(logo_url)
                if response.status_code == 200:  # Logo was successfully downloaded
                    img_temp.write(response.content)
                    img_temp.flush()
                    airline_company.logo.save(f"{iata_code}.png", File(img_temp))
                else:  # Logo was not available, use default image
                    airline_company.logo = '/airline_logos/airplanelogo.png'

                # Save airline company
                airline_company.save()

                self.stdout.write(self.style.SUCCESS(f"Successfully added airline company: {airline_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {airline_name}"))


    