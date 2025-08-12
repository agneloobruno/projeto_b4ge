from rest_framework import viewsets, generics, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from .models import Cidade, Estado, Obra, Material, InsumoAplicado
from .serializers import CidadeSerializer, EstadoSerializer, ObraSerializer, MaterialSerializer, UserSerializer, ImpactoPorEtapaSerializer, InsumoAplicadoSerializer
from .utils_calculo import atualizar_impacto_obra

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer

    def perform_create(self, serializer):
        obra = serializer.save()
        atualizar_impacto_obra(obra)

    def perform_update(self, serializer):
        obra = serializer.save()
        atualizar_impacto_obra(obra)

@api_view(['GET'])
def ping(request):
    return Response({"message": "ping from Django 🔁"})

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def atualizar_impacto_api(request, obra_id):
    try:
        obra = Obra.objects.get(id=obra_id)
    except Obra.DoesNotExist:
        return Response({"erro": "Obra não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    resultado = atualizar_impacto_obra(obra)
    return Response({"mensagem": resultado}, status=status.HTTP_200_OK)

@api_view(['POST'])
def adicionar_itens_obra(request, obra_id):
    obra = get_object_or_404(Obra, pk=obra_id)
    itens = request.data.get('itens', [])

    for i in itens:
        i['obra'] = obra.id
    
    ser = InsumoAplicadoSerializer(data=itens, many=True)
    ser.is_valid(raise_exception=True)
    ser.save()

    from .utils_calculo import atualizar_impacto_obra
    atualizar_impacto_obra(obra)

    return Response({"mensagem": "Itens adicionados com sucesso."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def impactos_por_obra(request, id):
    try:
        obra = Obra.objects.get(id=id)
    except Obra.DoesNotExist:
        return Response({"erro": "Obra não encontrada."}, status=status.HTTP_404_NOT_FOUND)

    dados_agrupados = (
        InsumoAplicado.objects
        .filter(obra=obra)
        .values("etapa_obra")
        .annotate(
            energia_embutida_total=Sum("energia_embutida_mj"),
            co2_total=Sum("co2_kg")
        )
        .order_by("etapa_obra")
    )

    por_etapa = [
        {
            "etapa_obra": row["etapa_obra"],
            "energia_embutida_total_gj": round((row["energia_embutida_mj"] or 0) / 1000.0, 4),
            "co2_total_kg": round(row["co2_kg"] or 0, 2),
        }
        for row in dados_agrupados
    ]

    totais = InsumoAplicado.objects.filter(obra=obra).aggregate(
        energia_mj=Sum("energia_embutida_mj"),
        co2_kg=Sum("co2_kg"),
    )

    return Response({
        "obra_id": obra.id,
        "por_etapa": por_etapa,
        "energia_total_gj": round((totais["energia_mj"] or 0) / 1000.0, 4),
        "co2_total_kg": round(totais["co2_kg"] or 0, 2),
    })

class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estado.objects.order_by('nome')
    serializer_class = EstadoSerializer

class CidadeViewSet(viewsets.ViewSet):
    def list(self, request, uf=None):
        if uf is None:
            return Response({"detail": "Estado (uf) não fornecido."}, status=400)

        cidades = Cidade.objects.filter(estado__sigla=uf.upper()).order_by('nome')
        serializer = CidadeSerializer(cidades, many=True)
        return Response(serializer.data)
