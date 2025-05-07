from django import forms
from .models import Obras, InsumoUsado

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obras
        fields = ['nome', 'tipologia', 'localizacao', 'area_construida']


class InsumoUsadoForm(forms.ModelForm):
    class Meta:
        model = InsumoUsado
        fields = ['obra', 'material', 'quantidade_kg']