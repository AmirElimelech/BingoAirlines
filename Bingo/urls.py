from . import views
from django.contrib import admin
from django.urls import path
from .views import flight_search
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from .views import login_view , home_view , logout_view , user_registration_view
from django.conf import settings
from django.conf.urls.static import static
from .view import base_views , customer_views 
from .view.base_views import BaseViews
from .view.customer_views import CustomerViews








urlpatterns = [
    # path('', views.home, name='home'),
    path('flight_search', views.flight_search, name='flight_search'),
    path('search-flight/', views.search_form, name='search_form'),
    path('search-results/', views.handle_search_form_submission, name='search_results'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('register/', user_registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('', home_view, name='home'),
    path('logout/', logout_view, name='logout'),
    

    # Base views

    path('get_all_flights/', BaseViews.get_all_flights_view, name="get_all_flights_view"),
    path('get_flight_by_id/<int:flight_id>/', BaseViews.get_flight_by_id_view, name="get_flight_by_id_view"),
    path('get_flights_by_parameters/<int:origin_country_id>/<int:destination_country_id>/<str:date>/', BaseViews.get_flights_by_parameters_view, name="get_flights_by_parameters_view"),
    path('get_all_airlines/', BaseViews.get_all_airlines_view, name="get_all_airlines_view"),
    path('get_airline_by_id/<int:airline_id>/', BaseViews.get_airline_by_id_view, name="get_airline_by_id_view"),
    path('get_all_countries/', BaseViews.get_all_countries_view, name="get_all_countries_view"),
    path('get_country_by_id/<int:country_id>/', BaseViews.get_country_by_id_view, name="get_country_by_id_view"),



     # Customer views
    path('update_customer/', CustomerViews.update_customer_view, name="update_customer_view"),
    path('add_ticket/', CustomerViews.add_ticket_view, name="add_ticket_view"),
    path('remove_ticket/<int:ticket_id>/', CustomerViews.remove_ticket_view, name="remove_ticket_view"),
    path('get_my_tickets/', CustomerViews.get_my_tickets_view, name="get_my_tickets_view"),
    # ... add other customer views here
    
    
    

]

# urlpatterns += static(settings.MEDIA_URL ,document_root =settings.MEDIA_ROOT)

if settings.DEBUG:  # Only serve media files in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)