
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ObraViewSet, MaterialViewSet,
    ping, RegisterView, atualizar_impacto_api
)

router = DefaultRouter()
router.register(r'obras', ObraViewSet, basename='obra')
router.register(r'materiais', MaterialViewSet, basename='material')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ping/', ping),
    path('api/registrar/', RegisterView.as_view(), name='registrar'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/obras/<int:obra_id>/atualizar_impacto/', atualizar_impacto_api, name='atualizar_impacto_api'),
]
