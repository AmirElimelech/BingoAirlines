from . import views
from django.contrib import admin
from django.urls import path
from .views import flight_search
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView




urlpatterns = [
    path('', views.home, name='home'),
    path('flight_search', views.flight_search, name='flight_search'),
    path('search-flight/', views.search_form, name='search_form'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('login/', LoginView.as_view(template_name='Bingo/registration/login.html'), name='login'),





    # path('add_user/', add_user_view, name='add_user'),
    # path('show_users/', views.show_users, name='show_users'),
    # path('update_user/<int:pk>', views.update_user, name='update_user'),
    

]

urlpatterns += static(settings.MEDIA_URL ,document_root =settings.MEDIA_ROOT)