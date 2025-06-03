# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObraViewSet, simular_obra, MaterialViewSet, salvar_obra, simular_fundacao
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'materiais', MaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
    path('simular/', simular_obra),
    path('simular_fundacao/', simular_fundacao),
    path('salvar/', salvar_obra),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('api/simular_fundacao/', simular_fundacao, name='simular_fundacao'),
]
