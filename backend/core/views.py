from rest_framework import viewsets, generics, serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Cidade, Estado, Obra, Material, InsumoAplicado
from .serializers import CidadeSerializer, EstadoSerializer, ObraSerializer, MaterialSerializer, UserSerializer, ImpactoPorEtapaSerializer
from .utils_calculo import atualizar_impacto_obra

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
def ping(request):
    return Response({"message": "pong from Django 🔁"})

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

    serializer = ImpactoPorEtapaSerializer(dados_agrupados, many=True)
    return Response({
        "obra": obra.nome,
        "etapas": serializer.data
    })

class EstadoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Estado.objects.order_by('nome')
    serializer_class = EstadoSerializer

class CidadeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CidadeSerializer

    def get_queryset(self):
        uf = self.kwargs.get('uf')
        if not uf:
            return Cidade.objects.none()
        return Cidade.objects.filter(estado__sigla__iexact=uf).order_by('nome')
