from django.contrib import admin
from .models import (
    Estado, Cidade, Obra, Material, ConversaoMaterial, Composicao,
    ItemDeComposicao, DistanciaInsumoCidade, ParametrosOperacionais,
    FatorTransporte, Desperdicio
)

admin.site.register(Estado)
admin.site.register(Cidade)
admin.site.register(Obra)
admin.site.register(Material)
admin.site.register(ConversaoMaterial)
admin.site.register(Composicao)
admin.site.register(ItemDeComposicao)
admin.site.register(DistanciaInsumoCidade)
admin.site.register(ParametrosOperacionais)
admin.site.register(FatorTransporte)
admin.site.register(Desperdicio)
