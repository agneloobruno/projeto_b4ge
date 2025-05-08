# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObraViewSet, simular_obra

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')

urlpatterns = [
    path('', include(router.urls)),
    path('simular/', simular_obra),
]
