from django import forms
from .models import Obras

class ObraForm(forms.ModelForm):
    class Meta:
        model = Obras
        fields = ['nome', 'tipologia', 'localizacao', 'area_construida']
