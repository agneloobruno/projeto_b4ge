from django.contrib import admin
from django.urls import path, include
from core.views import home, nova_obra, novo_insumo, ping

urlpatterns = [
    path('', home, name='home'),
    path('nova-obra/', nova_obra, name='nova_obra'),
    path('novo-insumo/', novo_insumo, name='novo_insumo'),
    path('api/ping/', ping),  # pode remover esse se já está no DRF
    path('api/', include('core.urls')),
    path('admin/', admin.site.urls),
]
