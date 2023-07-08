import pandas as pd
from django.core.management.base import BaseCommand
from Bingo.models import Airport

class Command(BaseCommand):
    help = 'Loads airports from airports.csv file into the database'

    def handle(self, *args, **options):
        df = pd.read_csv('Bingo/management/commands/airportspopulate.csv')

        for index, row in df.iterrows():
            try:
                airport = Airport(name=row['Airport'], iata_code=row['IATA code'])
                airport.save()
            except Exception as e:
                print(f"Error on row {index}: {row}")
                print(f"Exception: {e}")
