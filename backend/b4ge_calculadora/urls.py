from core.views import home, nova_obra, novo_insumo, ping
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('nova-obra/', nova_obra, name='nova_obra'),
    path('novo-insumo/', novo_insumo, name='novo_insumo'),
    path('api/ping/', ping),
    path('admin/', admin.site.urls),
]
