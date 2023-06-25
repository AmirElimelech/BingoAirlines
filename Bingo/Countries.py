import pandas as pd
from Bingo.models import Countries  # replace with your actual models module

df = pd.read_csv('countries.csv')

for index, row in df.iterrows():
    country = Countries(name=row['Country name'], country_code=row['Country Code'])
    country.save()