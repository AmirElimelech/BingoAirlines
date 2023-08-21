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
    


]

# urlpatterns += static(settings.MEDIA_URL ,document_root =settings.MEDIA_ROOT)

if settings.DEBUG:  # Only serve media files in debug mode
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)