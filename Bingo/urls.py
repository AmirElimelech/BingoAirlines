from django.urls import path
from .views import  handle_search_form_submission , autocomplete




urlpatterns = [

    # Search Form
    path('search-results/', handle_search_form_submission, name='search_results'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    
   
    


]


