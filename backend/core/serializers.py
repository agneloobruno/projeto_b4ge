from rest_framework import serializers
from .models import Obras, Material, Insumo, ItemLista, Composicao, ComposicaoItem


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class InsumoSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)

    class Meta:
        model = Insumo
        fields = '__all__'


class ItemListaSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer(read_only=True)
    insumo_id = serializers.PrimaryKeyRelatedField(
        source='insumo',
        queryset=Insumo.objects.all(),
        write_only=True,
        required=False
    )

    energia_embutida_gj_calculada = serializers.SerializerMethodField()
    co2_kg_calculado = serializers.SerializerMethodField()

    class Meta:
        model = ItemLista
        fields = [
            'id', 'obra', 'tipo', 'etapa_obra', 'insumo', 'insumo_id', 'composicao', 'unidade',
            'proporcao', 'quantidade', 'equivalente_kg',
            'energia_embutida_mj', 'energia_embutida_gj', 'energia_embutida_gj_calculada',
            'co2_kg', 'co2_kg_calculado',
            'distancia_km', 'energia_transporte_mj', 'energia_transporte_gj',
            'potencia_w', 'tempo_uso', 'energia_equip_mj', 'energia_equip_gj',
            'percentual_total'
        ]



class ObrasSerializer(serializers.ModelSerializer):
    energia_embutida_total = serializers.SerializerMethodField()
    co2_total = serializers.SerializerMethodField()
    itens_lista = ItemListaSerializer(many=True, read_only=True)

    class Meta:
        model = Obras
        fields = '__all__'

    def get_energia_embutida_total(self, obj):
        return obj.energia_embutida_total()

    def get_co2_total(self, obj):
        return obj.co2_total()


class ComposicaoItemSerializer(serializers.ModelSerializer):
    insumo = InsumoSerializer()
    subcomposicao = serializers.StringRelatedField()

    class Meta:
        model = ComposicaoItem
        fields = ['insumo', 'subcomposicao', 'unidade', 'proporcao']


class ComposicaoSerializer(serializers.ModelSerializer):
    itens = ComposicaoItemSerializer(many=True, read_only=True, source='itens')

    class Meta:
        model = Composicao
        fields = ['codigo', 'descricao', 'unidade', 'etapa_obra', 'itens']
