from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms.models import BaseInlineFormSet

from .models import (
    Obras, Material, Insumo, ItemLista, Cidade,
    DistanciaTransporte, Composicao, ComposicaoItem
)


class ItemListaInline(admin.TabularInline):
    model = ItemLista
    extra = 0
    fields = (
        'tipo', 'etapa_obra', 'insumo', 'composicao', 'unidade',
        'quantidade', 'proporcao', 'energia_embutida_gj', 'co2_kg'
    )
    readonly_fields = ('energia_embutida_gj', 'co2_kg')
    can_delete = False
    show_change_link = True


@admin.register(Obras)
class ObrasAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'tipologia', 'estado', 'municipio',
        'area_total_construir', 'data_inicio_construcao',
        'data_termino_construcao', 'energia_embutida_total', 'co2_total'
    )
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


@admin.register(Insumo)
class InsumoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sinapi', 'descricao', 'unidade', 'material')
    search_fields = ('codigo_sinapi', 'descricao')
    list_filter = ('unidade', 'material')


@admin.register(ItemLista)
class ItemListaAdmin(admin.ModelAdmin):
    list_display = (
        'obra', 'tipo', 'etapa_obra', 'insumo', 'composicao',
        'unidade', 'quantidade', 'proporcao',
        'energia_embutida_gj', 'co2_kg'
    )
    search_fields = ('obra__nome', 'insumo__descricao', 'etapa_obra', 'composicao__descricao')
    list_filter = ('obra', 'tipo', 'etapa_obra', 'insumo__descricao')
    readonly_fields = (
        'energia_embutida_mj', 'energia_embutida_gj',
        'energia_transporte_mj', 'energia_transporte_gj',
        'energia_equip_mj', 'energia_equip_gj',
        'equivalente_kg', 'co2_kg'
    )


# ➕ Validação para impedir salvar sem proporção:
class ComposicaoItemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                proporcao = form.cleaned_data.get('proporcao')
                if proporcao in (None, ''):
                    raise ValidationError("Todos os itens da composição devem ter um valor de 'proporção'.")


class ComposicaoItemInline(admin.TabularInline):
    model = ComposicaoItem
    fk_name = 'composicao_pai'
    extra = 0
    fields = ('insumo', 'subcomposicao', 'quantidade', 'proporcao', 'unidade')
    autocomplete_fields = ('insumo', 'subcomposicao')
    formset = ComposicaoItemInlineFormSet
    can_delete = False


class EhServicoFilter(admin.SimpleListFilter):
    title = 'É serviço?'
    parameter_name = 'eh_servico'

    def lookups(self, request, model_admin):
        return (
            ('sim', 'Sim (é pai de outra composição)'),
            ('nao', 'Não (é subcomposição)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sim':
            return queryset.filter(itens__isnull=False).distinct()
        if self.value() == 'nao':
            return queryset.exclude(id__in=Composicao.objects.filter(itens__isnull=False).values_list('id', flat=True))
        return queryset

@admin.register(Composicao)
class ComposicaoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'descricao', 'unidade', 'etapa_obra')
    search_fields = ('descricao', 'codigo')
    list_filter = ('etapa_obra', EhServicoFilter)
    inlines = [ComposicaoItemInline]

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')
    search_fields = ('nome',)
    list_filter = ('estado',)


@admin.register(DistanciaTransporte)
class DistanciaTransporteAdmin(admin.ModelAdmin):
    list_display = ('insumo', 'cidade', 'km')
    search_fields = ('insumo__descricao', 'cidade__nome')
    list_filter = ('cidade__estado',)
