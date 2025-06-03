from django.contrib import admin
from .models import Obras, Material, ItemLista, Cidade, DistanciaTransporte, Composicao, ComposicaoItem

class ItemListaInline(admin.TabularInline):
    model = ItemLista
    extra = 0
    fields = ('tipo', 'etapa_obra', 'material', 'composicao', 'unidade', 'quantidade', 'proporcao', 'energia_embutida_gj', 'co2_kg')
    readonly_fields = ('energia_embutida_gj', 'co2_kg')
    can_delete = False
    show_change_link = True

@admin.register(Obras)
class ObrasAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipologia', 'estado', 'municipio', 'area_total_construir', 'data_inicio_construcao', 'data_termino_construcao', 'energia_embutida_total', 'co2_total')
    inlines = [ItemListaInline]
    search_fields = ('nome', 'tipologia', 'municipio')
    list_filter = ('tipologia', 'estado', 'municipio', 'data_inicio_construcao', 'data_termino_construcao')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = (
        'descricao', 'densidade', 'energia_embutida_mj_kg',
        'energia_embutida_mj_m3', 'co2_kg', 'fator_manutencao',
        'referencia', 'capacidade_caminhao', 'referencia_para_cuiaba'
    )
    search_fields = ('descricao', 'referencia', 'referencia_para_cuiaba')
    list_filter = ('referencia',)

@admin.register(ItemLista)
class ItemListaAdmin(admin.ModelAdmin):
    list_display = ('obra', 'tipo', 'etapa_obra', 'material', 'composicao', 'unidade', 'quantidade', 'proporcao', 'energia_embutida_gj', 'co2_kg')
    search_fields = ('obra__nome', 'material__descricao', 'etapa_obra', 'composicao__descricao')
    list_filter = ('obra', 'tipo', 'etapa_obra', 'material__descricao')
    readonly_fields = ('energia_embutida_mj', 'energia_embutida_gj', 'energia_transporte_mj', 'energia_transporte_gj', 'energia_equip_mj', 'energia_equip_gj', 'equivalente_kg', 'co2_kg')

class ComposicaoItemInline(admin.TabularInline):
    model = ComposicaoItem
    fk_name = 'composicao_pai'
    extra = 0
    fields = ('material', 'quantidade', 'unidade', 'subcomposicao')
    autocomplete_fields = ('material', 'subcomposicao')
    can_delete = False

@admin.register(Composicao)
class ComposicaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'unidade', 'etapa_obra')
    search_fields = ('descricao', 'codigo')
    list_filter = ('etapa_obra',)  # corrigido aqui
    inlines = [ComposicaoItemInline]

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
