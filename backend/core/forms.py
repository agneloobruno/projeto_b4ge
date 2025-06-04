from django import forms
from .models import Obras, ItemLista

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obras
        fields = ['nome', 'tipologia', 'estado', 'municipio', 'area_total_construir']

class ItemListaForm(forms.ModelForm):
    class Meta:
        model = ItemLista
        fields = ['obra', 'tipo', 'etapa_obra', 'insumo', 'composicao', 'quantidade', 'unidade']
