import pandas as pd
from django.core.management.base import BaseCommand
from Bingo.models import Countries

class Command(BaseCommand):
    help = 'Loads countries from countries.csv file into the database'

    def handle(self, *args, **options):
        df = pd.read_csv('Bingo/management/commands/countries.csv')

        for index, row in df.iterrows():
            try:
                country = Countries(name=row['Country name'], country_code=row['Country Code'])
                country.save()
            except Exception as e:
                print(f"Error on row {index}: {row}")
                print(f"Exception: {e}")