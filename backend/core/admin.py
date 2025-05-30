from django.contrib import admin
from .models import Obras, Material, InsumoUsado, Cidade, DistanciaTransporte

@admin.register(Obras)
class ObrasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipologia', 'localizacao', 'area_construida')
    search_fields = ('nome', 'tipologia', 'localizacao')
    list_filter = ('tipologia',)

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descricao', 'densidade', 'energia_embutida_mj_kg',
        'energia_embutida_mj_m3', 'co2_kg', 'fator_manutencao',
        'referencia', 'capacidade_caminhao', 'referencia_para_cuiaba'
    )
    search_fields = ('descricao', 'referencia', 'referencia_para_cuiaba')
    list_filter = ('referencia',)

@admin.register(InsumoUsado)
class InsumoUsadoAdmin(admin.ModelAdmin):
    list_display = ('obra', 'material', 'quantidade_kg')
    search_fields = ('obra__nome', 'material__descricao')
    list_filter = ('obra',)

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)
    list_filter = ('estado',)

@admin.register(DistanciaTransporte)
class DistanciaTransporteAdmin(admin.ModelAdmin):
    list_display = ('material', 'cidade', 'km')
    search_fields = ('material__descricao', 'cidade__nome')
    list_filter = ('cidade__estado',)
