from django.shortcuts import render, redirect
from .models import Obras, InsumoUsado, Material
from .forms import ObraForm, InsumoUsadoForm
from django.http import JsonResponse
from .serializers import ObrasSerializer, MaterialSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ModelSerializer

def home(request):
    obras = Obras.objects.all()
    return render(request, 'core/home.html', {'obras': obras})

def nova_obra(request):
    form = ObraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'core/nova_obra.html', {'form': form})

def novo_insumo(request):
    form = InsumoUsadoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'core/novo_insumo.html', {'form': form})


@api_view(['GET'])
def ping(request):
    return Response({"message": "pong from Django 🔁"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simular_obra(request):
    dados = request.data
    insumos = dados.get('insumos', [])

    energia_total = 0
    co2_total = 0

    for insumo in insumos:
        material_id = insumo.get('material')
        quantidade = float(insumo.get('quantidade_kg', 0))

        # Puxa os dados do material relacionado
        from .models import Material
        try:
            mat = Material.objects.get(id=material_id)
            energia_total += quantidade * mat.energia_embutida_mj_kg * mat.fator_manutencao
            co2_total += quantidade * mat.co2eq_kg * mat.fator_manutencao
        except Material.DoesNotExist:
            continue  # ignora se material não encontrado

    return Response({
        "energia_total": round(energia_total, 2),
        "co2_total": round(co2_total, 2)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def salvar_obra(request):
    dados = request.data
    insumos = dados.get('insumos', [])

    # Cria a Obra
    obra = Obras.objects.create(
        nome=dados['nome'],
        tipologia=dados['tipologia'],
        localizacao=dados['localizacao'],
        area_construida=dados['area_construida']
    )

    # Cria os insumos vinculados à obra
    for insumo in insumos:
        try:
            material = Material.objects.get(id=insumo['material'])
            InsumoUsado.objects.create(
                obra=obra,
                material=material,
                quantidade_kg=insumo['quantidade_kg']
            )
        except Material.DoesNotExist:
            continue  # ignora se material inválido

    return Response({"message": "Obra salva com sucesso!"}, status=status.HTTP_201_CREATED)


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obras.objects.all()
    serializer_class = ObrasSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        print("📨 Dados recebidos:", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            print("✅ Obra criada com sucesso")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("❌ Erros no serializer:", serializer.errors)
        print("🧾 Campos recebidos:", list(request.data.keys()))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MaterialViewSet(viewsets.ReadOnlyModelViewSet):  # Apenas GET (list/retrieve)
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]