from core.views import home, nova_obra
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('nova-obra/', nova_obra, name='nova_obra'),
    path('admin/', admin.site.urls),
]
