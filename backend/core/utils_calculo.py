# core/utils_calculo.py
from django.db.models import Sum
from django.apps import apps

def calcular_impacto_insumo(insumo_aplicado) -> dict:
    """
    Calcula os impactos para um item (insumo aplicado) SEM depender de imports de models no topo.
    Usa os dados já presentes no objeto (ex.: equivalente_kg, quantidade, distancia_km).
    Ajuste os fatores conforme sua base real.
    """
    quantidade = insumo_aplicado.quantidade or 0.0
    eq_kg = insumo_aplicado.equivalente_kg or 0.0

    # Fatores EXEMPLO (troque pelos da sua base/tabela de fatores):
    emb_mj = eq_kg * 20.0            # energia embutida por kg
    emb_gj = emb_mj / 1000.0
    co2 = eq_kg * 0.1                # CO₂ por kg

    transporte_mj = (insumo_aplicado.distancia_km or 0.0) * 0.05 * quantidade
    transporte_gj = transporte_mj / 1000.0

    # Consumo de equipamentos (placeholder):
    pot = 1000.0   # W
    tempo = 1.0    # h
    equip_mj = (pot * tempo) / 3600.0
    equip_gj = equip_mj / 1000.0

    return {
        "energia_embutida_mj": emb_mj,
        "energia_embutida_gj": emb_gj,
        "co2_kg": co2,
        "energia_transporte_mj": transporte_mj,
        "energia_transporte_gj": transporte_gj,
        "potencia_w": pot,
        "tempo_uso": tempo,
        "energia_equip_mj": equip_mj,
        "energia_equip_gj": equip_gj,
        "percentual_total": 0.0,
    }

def atualizar_impacto_obra(obra):
    """
    Atualiza SOMENTE os totais da obra agregando os itens.
    NÃO chama save() dos itens para evitar loop.
    """
    InsumoAplicado = apps.get_model("core", "InsumoAplicado")
    agg = InsumoAplicado.objects.filter(obra=obra).aggregate(
        energia_mj=Sum("energia_embutida_mj"),
        co2_kg=Sum("co2_kg"),
    )
    obra.energia_total_mj = agg["energia_mj"] or 0.0
    obra.co2_total_kg = agg["co2_kg"] or 0.0
    obra.save(update_fields=["energia_total_mj", "co2_total_kg"])
