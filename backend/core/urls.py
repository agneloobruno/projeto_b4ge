# core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CidadeViewSet, EstadoViewSet, ObraViewSet, MaterialViewSet,
    ping, RegisterView, atualizar_impacto_api, impactos_por_obra
)

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'materiais', MaterialViewSet, basename='material')
router.register(r'estados', EstadoViewSet, basename='estado')
router.register(r'cidades', CidadeViewSet, basename='cidade')

urlpatterns = [
    path('', include(router.urls)),  # ✅ agora não duplica
    path('ping/', ping),
    path('registrar/', RegisterView.as_view(), name='registrar'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('obras/<int:obra_id>/atualizar_impacto/', atualizar_impacto_api, name='atualizar_impacto_api'),
    path('impactos/obra/<int:id>/', impactos_por_obra, name='impactos_por_obra'),
    path('estados/<str:uf>/cidades/', CidadeViewSet.as_view({'get': 'list'}), name='estado-cidades'),
]
