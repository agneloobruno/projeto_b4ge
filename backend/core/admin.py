from django.contrib import admin
from .models import Obras, Material, InsumoUsado

admin.site.register(Obras)
admin.site.register(Material)
admin.site.register(InsumoUsado)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descricao', 'densidade', 'energia_embutida_mj_kg',
        'energia_embutida_mj_m3', 'co2_kg', 'fator_manutencao',
        'referencia', 'distancia_transporte_km', 'capacidade_caminhao_kg',
        'referencia_cuiaba'
    )
    search_fields = ('descricao', 'referencia', 'referencia_cuiaba')