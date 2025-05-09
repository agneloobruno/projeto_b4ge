# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObraViewSet, simular_obra, MaterialViewSet, salvar_obra

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'materiais', MaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
    path('simular/', simular_obra),
    path('salvar/', salvar_obra),
]
