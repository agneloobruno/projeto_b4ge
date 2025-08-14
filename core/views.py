from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import Optional
from .models import (
    Estado, Cidade, Obra, Material, ConversaoMaterial,
    Composicao, ItemDeComposicao, DistanciaInsumoCidade,
    ParametrosOperacionais, FatorTransporte, Desperdicio
)
from .serializers import (
    EstadoSerializer, CidadeSerializer, ObraSerializer, MaterialSerializer,
    ConversaoMaterialSerializer, ComposicaoSerializer, ItemDeComposicaoSerializer,
    DistanciaInsumoCidadeSerializer, ParametrosOperacionaisSerializer,
    FatorTransporteSerializer, DesperdicioSerializer
)
from .calc_engine import calcular_impactos_obra

class EstadoViewSet(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializer

class CidadeViewSet(viewsets.ModelViewSet):
    queryset = Cidade.objects.select_related('estado').all()
    serializer_class = CidadeSerializer

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer

    @action(detail=True, methods=['get'])
    def impactos(self, request, pk: Optional[str] = None) -> Response:
        # Checagem explícita para satisfazer o type checker (Pylance)
        if pk is None:
            return Response({'detail': 'id inválido (None).'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            obra_id: int = int(pk)
        except (TypeError, ValueError):
            return Response({'detail': 'id inválido (não numérico).'}, status=status.HTTP_400_BAD_REQUEST)

        payload = calcular_impactos_obra(obra_id)
        return Response(payload, status=status.HTTP_200_OK)
    
class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class ConversaoMaterialViewSet(viewsets.ModelViewSet):
    queryset = ConversaoMaterial.objects.select_related('material').all()
    serializer_class = ConversaoMaterialSerializer

class ComposicaoViewSet(viewsets.ModelViewSet):
    queryset = Composicao.objects.all()
    serializer_class = ComposicaoSerializer

class ItemDeComposicaoViewSet(viewsets.ModelViewSet):
    queryset = ItemDeComposicao.objects.select_related('composicao','material').all()
    serializer_class = ItemDeComposicaoSerializer

class DistanciaInsumoCidadeViewSet(viewsets.ModelViewSet):
    queryset = DistanciaInsumoCidade.objects.select_related('material','cidade').all()
    serializer_class = DistanciaInsumoCidadeSerializer

class ParametrosOperacionaisViewSet(viewsets.ModelViewSet):
    queryset = ParametrosOperacionais.objects.all()
    serializer_class = ParametrosOperacionaisSerializer

class FatorTransporteViewSet(viewsets.ModelViewSet):
    queryset = FatorTransporte.objects.all()
    serializer_class = FatorTransporteSerializer

class DesperdicioViewSet(viewsets.ModelViewSet):
    queryset = Desperdicio.objects.all()
    serializer_class = DesperdicioSerializer
