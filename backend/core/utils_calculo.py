from .models import InsumoAplicado, Material, DistanciaInsumoCidade, Obra
from .utils import calcular_impacto
from django.db.models import Q

def calcular_impacto_insumo(insumo_aplicado: InsumoAplicado) -> dict:
    """
    Retorna dicionário com todos os valores de impacto para um insumo aplicado.
    """
    # Lógica de cálculo (exemplo simplificado)
    quantidade = insumo_aplicado.quantidade or 0
    eq_kg = insumo_aplicado.equivalente_kg or 0
    # Buscar fatores do insumo ou composição...
    # Por simplicidade, valores fictícios:
    emb_mj = eq_kg * 20  # fator energético por kg
    emb_gj = emb_mj / 1000
    co2 = eq_kg * 0.1    # emissões por kg
    transporte_mj = (insumo_aplicado.distancia_km or 0) * 0.05 * quantidade
    transporte_gj = transporte_mj / 1000
    # Consumo de equipamentos (exemplo):
    pot = 1000  # W fixo ou obtido de equipamento
    tempo = 1   # horas de uso
    equip_mj = (pot * tempo) / 3600
    equip_gj = equip_mj / 1000
    # Percentual do total da obra será recalculado no método da obra
    return {
        'energia_embutida_mj': emb_mj,
        'energia_embutida_gj': emb_gj,
        'co2_kg': co2,
        'energia_transporte_mj': transporte_mj,
        'energia_transporte_gj': transporte_gj,
        'potencia_w': pot,
        'tempo_uso': tempo,
        'energia_equip_mj': equip_mj,
        'energia_equip_gj': equip_gj,
        'percentual_total': 0,
    }

@transaction.atomic
def atualizar_impacto_obra(obra):
    """
    Recalcula todos os impactos de uma obra inteira.
    """
    # Recalcula cada item (invoca save em cascata)
    for item in obra.itens_aplicados.all():
        item.save()
    # Atualiza totais na própria obra
    obra.calcular_impacto_total()