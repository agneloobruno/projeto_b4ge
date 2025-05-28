# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObraViewSet, simular_obra, MaterialViewSet, salvar_obra
from .views import RegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'materiais', MaterialViewSet, basename='material')

urlpatterns = [
    path('api/', include(router.urls)),
    path('simular/', simular_obra),
    path('salvar/', salvar_obra),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
]
