from rest_framework import serializers
from .models import Obras, Material, InsumoUsado

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
