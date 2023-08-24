from django.urls import path
from .views import base_views, customer_views, administrator_views, airline_views



urlpatterns = [
    # Base views
    path('flights/', base_views.get_all_flights_api, name='get_all_flights'),
    path('flights/<int:id>/', base_views.get_flight_by_id_api, name='get_flight_by_id'),
    path('flights/search/', base_views.get_flights_by_parameters_api, name='get_flights_by_parameters'),
    path('airlines/', base_views.get_all_airlines_api, name='get_all_airlines'),
    path('airlines/<str:iata_code>/', base_views.get_airline_by_id_api, name='get_airline_by_id'),
    path('countries/', base_views.get_all_countries_api, name='get_all_countries'),
    path('countries/<str:country_code>/', base_views.get_country_by_id_api, name='get_country_by_id'),
    
    
    # Customer views
    path('customer/update/', customer_views.update_customer_api, name='update_customer'),
    path('customer/tickets/add/', customer_views.add_ticket_api, name='add_ticket'),
    path('customer/tickets/<int:ticket_id>/remove/', customer_views.remove_ticket_api, name='remove_ticket'),
    path('customer/tickets/', customer_views.get_my_tickets_api, name='get_my_tickets'),

    # Administrator views
    path('admin/customers/', administrator_views.get_all_customers_api, name='get_all_customers'),
    path('admin/airlines/add/', administrator_views.add_airline_api, name='add_airline'),
    path('admin/customers/add/', administrator_views.add_customer_api, name='add_customer'),
    path('admin/administrators/add/', administrator_views.add_administrator_api, name='add_administrator'),
    path('admin/airlines/<str:iata_code>/remove/', administrator_views.remove_airline_api, name='remove_airline'),
    path('admin/customers/<int:customer_id>/remove/', administrator_views.remove_customer_api, name='remove_customer'),
    path('admin/administrators/<int:admin_id>/remove/', administrator_views.remove_administrator_api, name='remove_administrator'),

    # Airline Company views
    path('airline/flights/', airline_views.get_my_flights_api, name='get_my_flights'),
    path('airline/flights/add/', airline_views.add_flight_api, name='add_flight'),
    path('airline/flights/update/', airline_views.update_flight_api, name='update_flight'),
    path('airline/flights/<int:flight_id>/remove/', airline_views.remove_flight_api, name='remove_flight'),
]

