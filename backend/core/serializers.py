from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cidade, Estado, Obra, Material, Insumo, InsumoAplicado, Composicao, ItemDeComposicao

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class InsumoSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Insumo
        fields = '__all__'

class InsumoAplicadoSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer(read_only=True)
    insumo_id = serializers.PrimaryKeyRelatedField(
        source='insumo',
        queryset=Insumo.objects.all(),
        write_only=True,
        required=False
    )

    class Meta:
        model = InsumoAplicado
        fields = '__all__'

class ObraSerializer(serializers.ModelSerializer):
    energia_embutida_total = serializers.SerializerMethodField()
    co2_total = serializers.SerializerMethodField()
    itens_aplicados = InsumoAplicadoSerializer(many=True, read_only=True)

    class Meta:
        model = Obra
        fields = '__all__'

    def get_energia_embutida_total(self, obj):
        return obj.energia_embutida_total()

    def get_co2_total(self, obj):
        return obj.co2_total()

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