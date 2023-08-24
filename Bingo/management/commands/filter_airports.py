from django.core.management.base import BaseCommand
import json

class Command(BaseCommand):
    help = 'Filters out airports with empty iata values from the JSON file.'

    def handle(self, *args, **kwargs):
        # Define the path to your JSON file
        file_path = "Bingo/management/commands/airportsandcountries.json"

        # Read the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Filter out entries with empty 'iata' values
        filtered_data = {key: value for key, value in data.items() if value['iata']}

        # Write the filtered data back to the JSON file
        with open(file_path, 'w') as file:
            json.dump(filtered_data, file, indent=4)

        self.stdout.write(self.style.SUCCESS('File has been updated!'))
