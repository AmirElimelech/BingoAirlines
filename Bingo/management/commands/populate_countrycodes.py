import json
from django.core.management.base import BaseCommand
from Bingo.models import Airport

class Command(BaseCommand):
    help = 'Populate country codes for airports from the provided JSON file.'

    def handle(self, *args, **options):
        # Load the JSON file
        with open('Bingo/management/commands/airportsandcountries.json', 'r') as file:
            data = json.load(file)

        # Iterate over each airport in the database
        for airport in Airport.objects.all():
            # Check if the airport's IATA code exists in the JSON data
            airport_data = next((item for key, item in data.items() if item["iata"] == airport.iata_code), None)
            
            # If found, update the country code
            if airport_data:
                airport.country_code = airport_data['country']
                self.stdout.write(self.style.SUCCESS(f'Successfully updated country code for: {airport.name}'))
            else:
                airport.country_code = "ZZ"
                self.stdout.write(self.style.WARNING(f'Could not find country code for: {airport.name}. Setting default value to "ZZ".'))

            airport.save()

        self.stdout.write(self.style.SUCCESS('Finished updating country codes.'))
