from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EstadoViewSet, CidadeViewSet, ObraViewSet, MaterialViewSet,
    ConversaoMaterialViewSet, ComposicaoViewSet, ItemDeComposicaoViewSet,
    DistanciaInsumoCidadeViewSet, ParametrosOperacionaisViewSet,
    FatorTransporteViewSet, DesperdicioViewSet
)

router = DefaultRouter()
router.register(r'estados', EstadoViewSet)
router.register(r'cidades', CidadeViewSet)
router.register(r'obras', ObraViewSet)
router.register(r'materiais', MaterialViewSet)
router.register(r'conversoes', ConversaoMaterialViewSet)
router.register(r'composicoes', ComposicaoViewSet)
router.register(r'itens', ItemDeComposicaoViewSet)
router.register(r'distancias', DistanciaInsumoCidadeViewSet)
router.register(r'parametros', ParametrosOperacionaisViewSet)
router.register(r'fator-transporte', FatorTransporteViewSet)
router.register(r'desperdicios', DesperdicioViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
