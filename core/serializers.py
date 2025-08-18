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
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=Estado.objects.all(), source='estado', write_only=True
    )
    class Meta:
        model = Cidade
        fields = ('id', 'nome', 'codigo_ibge', 'estado', 'estado_id')

class ObraSerializer(serializers.ModelSerializer):
    # leitura: exibe o id da cidade
    cidade = serializers.PrimaryKeyRelatedField(read_only=True)

    # escrita: aceita cidade_id e mapeia para o campo relacional 'cidade'
    cidade_id = serializers.PrimaryKeyRelatedField(
        queryset=Cidade.objects.all(), source='cidade', write_only=True
    )

    # força conversão correta para Decimal
    area_construida_m2 = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    class Meta:
        model = Obra
        fields = (
            'id', 'nome', 'area_construida_m2',
            'fundacao_codigo',
            'supra_estrutura_1_codigo',
            'supra_estrutura_2_codigo',
            'fechamentos_codigo',
            'telhado_codigo',
            'piso_codigo',
            'created_at', 'updated_at',
            'cidade', 'cidade_id',
        )


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
