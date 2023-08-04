from django.db import models


class LoginToken(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    role = models.CharField(
        choices=[("customer", "Customer"), ("airline", "Airline"), ("admin", "Admin")],
        max_length=10,
    )

    def __str__(self):
        return f"{self.name} - {self.role}"
