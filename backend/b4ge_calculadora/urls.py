from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.views import ObraViewSet, home, nova_obra, novo_insumo, ping

# Criando o router para o DRF
router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')

urlpatterns = [
    path('', home, name='home'),
    path('nova-obra/', nova_obra, name='nova_obra'),
    path('novo-insumo/', novo_insumo, name='novo_insumo'),
    path('api/', include(router.urls)),
    path('api/ping/', ping),
    path('admin/', admin.site.urls),
]
