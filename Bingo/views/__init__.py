

# # Importing authentication-related views from auth_views.py
# from .auth_views import home_view, user_registration_view, login_view, logout_view

# # Importing flight-related views from flight_views.py
# from .flight_views import search_form, flight_search, autocomplete

from .auth_views import home_view, user_registration_view, login_view, logout_view
from .flight_views import search_form, flight_search, autocomplete, handle_search_form_submission , get_iata_code