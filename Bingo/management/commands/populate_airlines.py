
# import pandas as pd
# from django.core.management.base import BaseCommand
# from Bingo.models import Users

# class Command(BaseCommand):
#     help = 'Loads airlines from airlineuserspopulate.csv file into the database'

#     def handle(self, *args, **options):
#         # df = pd.read_csv('Bingo/management/commands/airlineuserspopulate.csv')
#         df = pd.read_csv('Bingo/management/commands/airlineuserspopulate.csv', dtype={'ID': 'Int64'})

#         for index, row in df.iterrows():
#             iata_code = row['IATA']
#             airline_name = row['Airline']
#             country_name = row['Country']
#             airline_id = str(row['ID']).zfill(9)  # Pad the ID with leading zeros

#             # Check if airline_name is a valid string
#             if isinstance(airline_name, str):
#                 # Generate email and password based on airline name
#                 email = airline_name.lower().replace(" ", "") + "@mail.com"
#                 password = airline_name.lower().replace(" ", "")

#                 # Check if the user with the same email already exists
#                 if Users.objects.filter(email=email).exists():
#                     self.stdout.write(self.style.WARNING(f"Skipping duplicate entry: {airline_name} ({email})"))
#                     continue

#                 # Check if the user with the same username already exists
#                 if Users.objects.filter(username=airline_name).exists():
#                     self.stdout.write(self.style.WARNING(f"Skipping duplicate entry: {airline_name}"))
#                     continue

#                 # Create a new user
#                 user = Users(id=airline_id, username=airline_name, email=email, user_role_id=2)  # Assuming user_role_id 2 corresponds to the airline company role
#                 user.password = password  # Set the user's password
#                 user.save()

#                 self.stdout.write(self.style.SUCCESS(f"Successfully added user: {airline_name}"))
#             else:
#                 self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {airline_name}"))





import re
from django.contrib.auth.hashers import make_password
import pandas as pd
from django.core.management.base import BaseCommand
from Bingo.models import Users

class Command(BaseCommand):
    help = 'Loads airlines from airlineuserspopulate.csv file into the database'

    def handle(self, *args, **options):
        df = pd.read_csv('Bingo/management/commands/airlineuserspopulate.csv', dtype={'ID': 'Int64'})

        password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$"

        for index, row in df.iterrows():
            iata_code = row['IATA']
            airline_name = row['Airline']
            country_name = row['Country']
            airline_id = str(row['ID']).zfill(9)  # Pad the ID with leading zeros

            if isinstance(airline_name, str):
                # Generate email and password based on airline name
                email = airline_name.lower().replace(" ", "") + "@mail.com"
                generated_password = airline_name.lower().replace(" ", "") + "A1!"

                # Validate generated password against pattern
                if len(generated_password) < 6 or not re.match(password_pattern, generated_password):
                    self.stdout.write(self.style.WARNING(f"Generated password doesn't meet requirements for: {airline_name}"))
                    continue

                hashed_password = make_password(generated_password)

                # Check if the user with the same email already exists
                if Users.objects.filter(email=email).exists():
                    self.stdout.write(self.style.WARNING(f"Skipping duplicate entry: {airline_name} ({email})"))
                    continue

                # Check if the user with the same username already exists
                if Users.objects.filter(username=airline_name).exists():
                    self.stdout.write(self.style.WARNING(f"Skipping duplicate entry: {airline_name}"))
                    continue

                # Create a new user
                user = Users(id=airline_id, username=airline_name, email=email, user_role_id=2)  # Assuming user_role_id 2 corresponds to the airline company role
                user.password = hashed_password  # Set the user's hashed password
                user.save()

                self.stdout.write(self.style.SUCCESS(f"Successfully added user: {airline_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Skipping invalid entry: {airline_name}"))
