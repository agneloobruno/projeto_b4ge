from rest_framework import serializers
from .models import Obras, Material, InsumoUsado

class ObrasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obras
        fields = '__all__'

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'
