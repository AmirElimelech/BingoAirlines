import pandas as pd
from django.core.management.base import BaseCommand
from Bingo.models import Airport

class Command(BaseCommand):
    help = 'Loads airports from airports.csv file into the database'

    def handle(self, *args, **options):
        df = pd.read_csv('Bingo/management/commands/airportspopulate.csv')

        for index, row in df.iterrows():
            try:
                airport, created = Airport.objects.get_or_create(iata_code=row['IATA code'],
                                                                  defaults={'name': row['Airport']})

                if not created:
                    print(f"Airport with IATA code {row['IATA code']} already exists. Skipped.")

            except Exception as e:
                print(f"Error on row {index}: {row}")
                print(f"Exception: {e}")