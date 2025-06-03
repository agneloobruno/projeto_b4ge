from rest_framework import serializers
from .models import Obras, Material, ItemLista, Composicao, ComposicaoItem

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class ItemListaSerializer(serializers.ModelSerializer):
    material = MaterialSerializer(read_only=True)  # mostra dados do material
    material_id = serializers.PrimaryKeyRelatedField(
        source='material',
        queryset=Material.objects.all(),
        write_only=True,
        required=False
    )

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
