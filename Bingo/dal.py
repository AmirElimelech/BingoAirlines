from .models import Flights, Countries, Tickets, Airline_Companies, Customers, Users, User_Roles, Administrators
from django.core.exceptions import ObjectDoesNotExist

class DAL:
    def __init__(self, model):
        self.model = model

    def get_by_id(self, id):
        try:
            return self.model.objects.get(id=id)
        except ObjectDoesNotExist:
            return None

    def get_all(self):
        return self.model.objects.all()

    def add(self, **kwargs):
        return self.model.objects.create(**kwargs)

    def add_all(self, objects):
        return self.model.objects.bulk_create(objects)

    def update(self, id, **kwargs):
        try:
            instance = self.model.objects.get(id=id)
            for key, value in kwargs.items():
                setattr(instance, key, value)
            instance.save()
            return instance
        except ObjectDoesNotExist:
            return None

    def remove(self, id):
        try:
            instance = self.model.objects.get(id=id)
            instance.delete()
            return True
        except ObjectDoesNotExist:
            return False



flights_dal = DAL(Flights)
countries_dal = DAL(Countries)
tickets_dal = DAL(Tickets)
airline_companies_dal = DAL(Airline_Companies)
customers_dal = DAL(Customers)
users_dal = DAL(Users)
user_roles_dal = DAL(User_Roles)
administrators_dal = DAL(Administrators)