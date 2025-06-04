from rest_framework import serializers
from .models import Obras, Material, ItemLista, Composicao, ComposicaoItem

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ItemListaSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)
    material_id = serializers.PrimaryKeyRelatedField(
        source='material',
        queryset=Material.objects.all(),
        write_only=True,
        required=False
    )

    energia_embutida_gj_calculada = serializers.SerializerMethodField()
    co2_kg_calculado = serializers.SerializerMethodField()

    class Meta:
        model = ItemLista
        fields = '__all__' + ('energia_embutida_gj_calculada', 'co2_kg_calculado')

    def get_energia_embutida_gj_calculada(self, obj):
        if obj.material and obj.quantidade and obj.material.energia_embutida_mj_kg:
            fator = obj.material.fator_manutencao or 1
            return round((obj.quantidade * obj.material.energia_embutida_mj_kg * fator) / 1000, 4)
        return None

    def get_co2_kg_calculado(self, obj):
        if obj.material and obj.quantidade and obj.material.co2_kg:
            fator = obj.material.fator_manutencao or 1
            return round(obj.quantidade * obj.material.co2_kg * fator, 4)
        return None

    class Meta:
        model = ItemLista
        fields = '__all__'

class ObrasSerializer(serializers.ModelSerializer):
    energia_embutida_total = serializers.SerializerMethodField()
    co2_total = serializers.SerializerMethodField()
    class Meta:
        model = Obras
        fields = '__all__'

    def get_energia_embutida_total(self, obj):
        return obj.energia_embutida_total()

    def get_co2_total(self, obj):
        return obj.co2_total()

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ComposicaoItemSerializer(serializers.ModelSerializer):
    material = MaterialSerializer()

    class Meta:
        model = ComposicaoItem
        fields = ['material', 'quantidade', 'unidade']

class ComposicaoSerializer(serializers.ModelSerializer):
    itens = ComposicaoItemSerializer(many=True, read_only=True, source='composicaoitem_set')

    class Meta:
        model = Composicao
        fields = ['codigo', 'descricao', 'unidade', 'classe_1', 'classe_2', 'itens']
