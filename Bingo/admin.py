from django.contrib import admin
from .models import Flights, Countries, Tickets, Airline_Companies, Customers, Users, User_Roles, Administrators , Airport
from .models import Airline_Companies
import requests
from django.core.files import File
from io import BytesIO


class AirlineCompaniesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not obj.logo:  # If no logo file is uploaded
            url = f'https://content.r9cdn.net/rimg/provider-logos/airlines/v/{obj.iata_code}.png?crop=false&width=100&height=100'
            response = requests.get(url)
            if response.status_code == 200:
                # Save the logo to the ImageField
                img_temp = BytesIO()
                img_temp.write(response.content)
                img_temp.seek(0)
                obj.logo.save(f'{obj.iata_code}.png', File(img_temp), save=False)
        
        super().save_model(request, obj, form, change)


admin.site.register(Airline_Companies, AirlineCompaniesAdmin)
admin.site.register(Flights)
admin.site.register(Countries)
admin.site.register(Tickets)
admin.site.register(Customers)
admin.site.register(Users)
admin.site.register(User_Roles)
admin.site.register(Administrators)
admin.site.register(Airport)

