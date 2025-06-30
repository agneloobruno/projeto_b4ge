from django.contrib import admin
from .models import (
    Obra, Material, Insumo, InsumoAplicado, Cidade,
    DistanciaInsumoCidade, Composicao, ItemDeComposicao
)

class InsumoAplicadoInline(admin.TabularInline):
    model = InsumoAplicado
    extra = 0
    fields = (
        'tipo', 'etapa_obra', 'insumo', 'composicao', 'unidade',
        'quantidade', 'proporcao', 'energia_embutida_gj', 'co2_kg'
    )
    readonly_fields = ('energia_embutida_gj', 'co2_kg')
    can_delete = False
    show_change_link = True

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipologia', 'estado', 'cidade', 'area_total_construir', 'co2_total')
    inlines = [InsumoAplicadoInline]
    search_fields = ('nome', 'tipologia')
    list_filter = ('tipologia', 'estado')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'densidade', 'energia_embutida_mj_kg', 'co2_kg')
    search_fields = ('descricao',)
    list_filter = ('referencia',)

@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sinapi', 'descricao', 'unidade', 'material')
    search_fields = ('codigo_sinapi', 'descricao')
    list_filter = ('unidade', 'material')

@admin.register(InsumoAplicado)
class InsumoAplicadoAdmin(admin.ModelAdmin):
    list_display = (
        'obra', 'tipo', 'etapa_obra', 'insumo', 'composicao', 'unidade', 'quantidade', 'energia_embutida_gj', 'co2_kg'
    )
    search_fields = ('obra__nome', 'insumo__descricao')
    list_filter = ('obra', 'tipo', 'etapa_obra')
    readonly_fields = (
        'energia_embutida_mj', 'energia_embutida_gj',
        'energia_transporte_mj', 'energia_transporte_gj',
        'energia_equip_mj', 'energia_equip_gj', 'co2_kg'
    )

class ItemDeComposicaoInline(admin.TabularInline):
    model = ItemDeComposicao
    fk_name = 'composicao_pai'
    extra = 0
    fields = ('insumo', 'subcomposicao', 'quantidade', 'proporcao', 'unidade')
    autocomplete_fields = ('insumo', 'subcomposicao')
    can_delete = False

@admin.register(Composicao)
class ComposicaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'unidade', 'etapa_obra')
    search_fields = ('descricao', 'codigo')
    list_filter = ('etapa_obra',)
    inlines = [ItemDeComposicaoInline]

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)
    list_filter = ('estado',)

@admin.register(DistanciaInsumoCidade)
class DistanciaInsumoCidadeAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'cidade', 'km')
    search_fields = ('insumo__descricao', 'cidade__nome')
    list_filter = ('cidade__estado',)