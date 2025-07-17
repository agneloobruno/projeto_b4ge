from django.contrib import admin
from django.db.models import Q
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
    
# Filtro personalizado: define o que a composição contém
class TipoItemFilter(admin.SimpleListFilter):
    title = 'Contém'
    parameter_name = 'tipo_item'

    def lookups(self, request, model_admin):
        return [
            ('insumo', 'Apenas Insumos'),
            ('subcomposicao', 'Apenas Subcomposições'),
            ('ambos', 'Ambos'),
            ('nenhum', 'Nenhum'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'insumo':
            return queryset.filter(
                itens__insumo__isnull=False,
                itens__subcomposicao__isnull=True
            ).distinct()
        elif self.value() == 'subcomposicao':
            return queryset.filter(
                itens__insumo__isnull=True,
                itens__subcomposicao__isnull=False
            ).distinct()
        elif self.value() == 'ambos':
            return queryset.filter(
                Q(itens__insumo__isnull=False) & Q(itens__subcomposicao__isnull=False)
            ).distinct()
        elif self.value() == 'nenhum':
            return queryset.exclude(itens__isnull=False)
        return queryset

# Filtro personalizado: define se a composição é um serviço ou subcomposição
class TipoComposicaoFilter(admin.SimpleListFilter):
    title = 'Tipo'
    parameter_name = 'tipo_composicao'

    def lookups(self, request, model_admin):
        return [
            ('servico', 'Serviço (não é chamada por nenhuma outra)'),
            ('composicao', 'Composição (é chamada por outra)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'servico':
            return queryset.exclude(como_subcomposicao__isnull=False)
        elif self.value() == 'composicao':
            return queryset.filter(como_subcomposicao__isnull=False).distinct()
        return queryset

# Inline para mostrar os insumos e subcomposições
class ItemDeComposicaoInline(admin.TabularInline):
    model = ItemDeComposicao
    fk_name = 'composicao_pai'
    extra = 0
    fields = ('codigo', 'descricao', 'tipo', 'unidade', 'proporcao')
    readonly_fields = ('codigo', 'descricao', 'tipo')
    can_delete = False

    def codigo(self, obj):
        if obj.insumo:
            return obj.insumo.codigo_sinapi
        elif obj.subcomposicao:
            return obj.subcomposicao.codigo
        return "—"

    def descricao(self, obj):
        if obj.insumo:
            return obj.insumo.descricao
        elif obj.subcomposicao:
            return obj.subcomposicao.descricao
        return "—"

    def tipo(self, obj):
        if obj.insumo:
            return "INSUMO"
        elif obj.subcomposicao:
            return "COMPOSICAO"
        return "—"

@admin.register(Composicao)
class ComposicaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'unidade', 'etapa_obra', 'tipo_composicao', 'tipo_de_itens')
    search_fields = ('descricao', 'codigo')
    list_filter = ('etapa_obra', TipoItemFilter, TipoComposicaoFilter)
    inlines = [ItemDeComposicaoInline]

    def tipo_de_itens(self, obj):
        tem_insumo = obj.itens.filter(insumo__isnull=False).exists()
        tem_subcomposicao = obj.itens.filter(subcomposicao__isnull=False).exists()

        if tem_insumo and tem_subcomposicao:
            return "Insumos + Subcomposições"
        elif tem_insumo:
            return "Somente Insumos"
        elif tem_subcomposicao:
            return "Somente Subcomposições"
        else:
            return "Nenhum"
    tipo_de_itens.short_description = "Contém"

    def tipo_composicao(self, obj):
        if obj.como_subcomposicao.exists():
            return "Composição"
        return "Serviço"
    tipo_composicao.short_description = "Tipo"

@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipologia', 'estado', 'cidade', 'area_total_construir', 'co2_total')
    inlines = [InsumoAplicadoInline]
    search_fields = ('nome', 'tipologia')
    list_filter = ('tipologia', 'estado')



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
