from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from Bingo.models import Users

class Command(BaseCommand):
    help = 'Rehash all user passwords and append "A1!" to each password'

    def handle(self, *args, **options):
        users = Users.objects.all()
        for user in users:
            plain_password = user.password + "A1!"  # Append "A1!" to existing password
            user.password = make_password(plain_password)  # Hash the new password
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Successfully updated password for user: {user.username}"))

        self.stdout.write(self.style.SUCCESS("All user passwords have been successfully updated and rehashed."))