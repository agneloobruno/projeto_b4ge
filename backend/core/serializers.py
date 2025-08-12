from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cidade, Estado, Obra, Material, Insumo, InsumoAplicado, Composicao, ItemDeComposicao, EtapaConstrutiva

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Insumo
        fields = '__all__'

class InsumoAplicadoCreateSerializer(serializers.ModelSerializer):
    """Aceita apenas entradas brutas; derivados são read-only no output."""
    class Meta:
        model = InsumoAplicado
        fields = (
            "id","obra","etapa_obra","insumo","quantidade","unidade",
            "distancia_km","potencia_w","tempo_uso_h","percentual_desperdicio",
        )

class InsumoAplicadoSerializer(serializers.ModelSerializer):
    """Completo (somente leitura para os derivados)."""
    class Meta:
        model = InsumoAplicado
        fields = "__all__"
        read_only_fields = (
            "q_kg",
            "energia_material_mj","energia_transporte_mj","energia_equip_mj",
            "energia_desperdicio_mj","energia_transp_descarte_mj",
            "energia_total_mj","energia_total_gj",
            "co2_por_gj_kg","co2_material_kg","co2_total_fator_kg","co2_total_kg",
            "calculado_em",
        )

class EtapaConstrutivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtapaConstrutiva
        fields = "__all__"

    class Meta:
        model = InsumoAplicado
        fields = '__all__'

class ObraSerializer(serializers.ModelSerializer):
    energia_total_gj = serializers.SerializerMethodField()
    class Meta:
        model = Obra
        fields = "__all__"
    class Meta:
        model = Obra
        fields = '__all__'



    def get_energia_total_gj(self, obj):
        return round((obj.energia_total_mj or 0) / 1000.0, 4)  # Convert to GJ

    def get_co2_total(self, obj):
        return round(obj.co2_total_kg or 0, 2) 
    
class ItemDeComposicaoSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    subcomposicao = serializers.StringRelatedField()

    class Meta:
        model = ItemDeComposicao
        fields = ['insumo', 'subcomposicao', 'unidade', 'proporcao']

class ComposicaoSerializer(serializers.ModelSerializer):
    itens = ItemDeComposicaoSerializer(many=True, read_only=True, source='itens')

    class Meta:
        model = Composicao
        fields = ['codigo', 'descricao', 'unidade', 'etapa_obra', 'itens']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class ImpactoPorEtapaSerializer(serializers.Serializer):
    etapa_obra = serializers.CharField()
    energia_embutida_total = serializers.FloatField()
    co2_total = serializers.FloatField()


class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = ['sigla', 'nome']  # ou os campos que você tenha

class CidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cidade
        fields = ['id', 'nome']