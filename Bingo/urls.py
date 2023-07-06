from . import views
from django.contrib import admin
from django.urls import path
from .views import flight_search
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('flight_search', views.flight_search, name='flight_search'),




    # path('add_user/', add_user_view, name='add_user'),
    # path('show_users/', views.show_users, name='show_users'),
    # path('update_user/<int:pk>', views.update_user, name='update_user'),
    

]

urlpatterns += static(settings.MEDIA_URL ,document_root =settings.MEDIA_ROOT)