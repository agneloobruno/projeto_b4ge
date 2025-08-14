from rest_framework import serializers
from .models import (
    Estado, Cidade, Obra, Material, ConversaoMaterial,
    Composicao, ItemDeComposicao, DistanciaInsumoCidade,
    ParametrosOperacionais, FatorTransporte, Desperdicio
)

class EstadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estado
        fields = '__all__'

class CidadeSerializer(serializers.ModelSerializer):
    estado = EstadoSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(queryset=Estado.objects.all(), source='estado', write_only=True)
    class Meta:
        model = Cidade
        fields = ('id','nome','codigo_ibge','estado','estado_id')

class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ConversaoMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversaoMaterial
        fields = '__all__'

class ComposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composicao
        fields = '__all__'

class ItemDeComposicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDeComposicao
        fields = '__all__'

class DistanciaInsumoCidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanciaInsumoCidade
        fields = '__all__'

class ParametrosOperacionaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParametrosOperacionais
        fields = '__all__'

class FatorTransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FatorTransporte
        fields = '__all__'

class DesperdicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desperdicio
        fields = '__all__'
