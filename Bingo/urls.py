from . import views
from django.contrib import admin
from django.urls import path
from .views import flight_search
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView
from .views import login_view
from .views import register_view






urlpatterns = [
    path('', views.home, name='home'),
    path('flight_search', views.flight_search, name='flight_search'),
    path('search-flight/', views.search_form, name='search_form'),
    path('search-results/', views.handle_search_form_submission, name='search_results'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('customer_portal/', views.customer_portal, name='customer_portal'),
 




    # path('add_user/', add_user_view, name='add_user'),
    # path('show_users/', views.show_users, name='show_users'),
    # path('update_user/<int:pk>', views.update_user, name='update_user'),
    

]

urlpatterns += static(settings.MEDIA_URL ,document_root =settings.MEDIA_ROOT)