from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import login_view , home_view , logout_view , user_registration_view 
from .views import search_form , handle_search_form_submission , autocomplete




urlpatterns = [
    

    # Authentication and home page
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', user_registration_view, name='register'),

    # Search Form
    path('search-flight/', search_form, name='search_form'),
    path('search-results/', handle_search_form_submission, name='search_results'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    
   
    


]


if settings.DEBUG:  # Only serve media files in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)