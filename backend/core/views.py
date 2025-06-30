from django.shortcuts import render, redirect
from .models import Obras, Material, ItemLista, Composicao
from .forms import ObraForm
from django.http import JsonResponse
from .serializers import ObrasSerializer, MaterialSerializer
from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
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

@api_view(['GET'])
def ping(request):
    return Response({"message": "pong from Django 🔁"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def simular_obra(request):
    dados = request.data
    area_fundacao = float(dados.get('area_fundacao', 0))

    energia_total = 0
    co2_total = 0
    itens_calculados = []

    # Substituir por lógica de composição futuramente
    materiais_base = [
        {"material_id": 1, "descricao": "Cimento", "proporcao": 50},
        {"material_id": 2, "descricao": "Brita", "proporcao": 100},
    ]

    for mat in materiais_base:
        try:
            material = Material.objects.get(id=mat["material_id"])
        except Material.DoesNotExist:
            continue

        quantidade = area_fundacao * mat["proporcao"]
        energia = quantidade * (material.energia_embutida_mj_kg or 0) * (material.fator_manutencao or 1)
        co2 = quantidade * (material.co2_kg or 0) * (material.fator_manutencao or 1)

        energia_total += energia
        co2_total += co2

        itens_calculados.append({
            "material": material.descricao,
            "quantidade": round(quantidade, 2),
            "energia": round(energia, 2),
            "co2": round(co2, 2),
        })

    return Response({
        "itens": itens_calculados,
        "energia_total_mj": round(energia_total, 2),
        "co2_total_kg": round(co2_total, 2)
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def salvar_obra(request):
    dados = request.data
    etapas_tecnicas = dados.get('etapas_tecnicas', [])

    # Validação básica
    campos_obrigatorios = ['nome', 'tipologia', 'estado', 'cidade', 'area_total_construir']
    faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    if faltando:
        return Response({"erro": f"Campos obrigatórios ausentes: {', '.join(faltando)}"}, status=400)

    try:
        obra = Obras.objects.create(
            nome=dados.get('nome'),
            tipologia=dados.get('tipologia'),
            estado=dados.get('estado'),
            cidade=dados.get('cidade'),
            area_total_construir=dados.get('area_total_construir')
        )
    except Exception as e:
        return Response({"erro": f"Erro ao criar obra: {str(e)}"}, status=500)

    # Salva cada etapa técnica recebida
    for etapa in etapas_tecnicas:
        nome = etapa.get('nome')
        dados_json = etapa.get('dados')
        if nome and dados_json:
            EtapaObra.objects.create(obra=obra, nome=nome, dados=dados_json)

    return Response({"message": "Obra e etapas salvas com sucesso!", "obra_id": obra.id}, status=status.HTTP_201_CREATED)

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

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class UserSerializer(ModelSerializer):
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
def simular_fundacao(request):
    codigo = request.data.get('codigo_composicao')
    multiplicador = float(request.data.get('multiplicador', 0))

    try:
        composicao = Composicao.objects.get(codigo=codigo)
    except Composicao.DoesNotExist:
        return Response({"error": "Composição não encontrada"}, status=404)

    total_co2 = 0
    itens_resultado = []
    visitados = set()

    def resolver_composicao(comp, mult):
        nonlocal total_co2
        if comp.pk in visitados:
            return  # previne ciclo
        visitados.add(comp.pk)

        for item in comp.itens.filter(valido=True):
            proporcao = item.proporcao or 0
            quantidade = proporcao * mult

            if item.insumo and item.insumo.material:
                mat = item.insumo.material
                co2 = quantidade * (mat.co2_kg or 0) * (mat.fator_manutencao or 1)
                total_co2 += co2
                itens_resultado.append({
                    "material": mat.descricao,
                    "quantidade_kg": round(quantidade, 2),
                    "co2_kg": round(co2, 2)
                })

            elif item.subcomposicao:
                resolver_composicao(item.subcomposicao, quantidade)

    resolver_composicao(composicao, multiplicador)

    return Response({
        "composicao": composicao.descricao,
        "codigo": composicao.codigo,
        "multiplicador_utilizado": multiplicador,
        "co2_total_kg": round(total_co2, 2),
        "itens": itens_resultado
    })