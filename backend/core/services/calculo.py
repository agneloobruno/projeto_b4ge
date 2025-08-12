from __future__ import annotations
from typing import Optional
from django.apps import apps

def _get_model(name: str):
    return apps.get_model("core", name)

def obter_parametro(chave: str, default: float) -> float:
    ParametroGlobal = _get_model("ParametroGlobal")
    try:
        return float(ParametroGlobal.objects.get(chave=chave).valor)
    except Exception:
        return float(default)

def obter_fator_transporte(nome: str, default: float) -> float:
    FatorTransporte = _get_model("FatorTransporte")
    try:
        return float(FatorTransporte.objects.get(nome=nome).mj_por_kg_km)
    except Exception:
        return float(default)

def desperdicio_default(material_id: Optional[int], etapa: Optional[str]) -> float:
    Desperdicio = _get_model("Desperdicio")
    if material_id:
        d = Desperdicio.objects.filter(material_id=material_id, etapa_obra=etapa).values_list("percentual", flat=True).first()
        if d is None:
            d = Desperdicio.objects.filter(material_id=material_id, etapa_obra__isnull=True).values_list("percentual", flat=True).first()
        if d is not None:
            return float(d)
    d2 = Desperdicio.objects.filter(material__isnull=True, etapa_obra=etapa).values_list("percentual", flat=True).first()
    return float(d2 or 0.0)

def normalizar_para_kg(quantidade: float, unidade: Optional[str], densidade_kg_m3: Optional[float]) -> float:
    if not quantidade:
        return 0.0
    u = (unidade or "").lower()
    if u == "kg":
        return float(quantidade)
    if u == "t":
        return float(quantidade) * 1000.0
    if u == "m3":
        dens = float(densidade_kg_m3 or 0.0)
        return float(quantidade) * dens if dens > 0 else 0.0
    if u in ("l", "lt"):
        dens = float(densidade_kg_m3 or 0.0)
        return float(quantidade) * (dens / 1000.0) if dens > 0 else 0.0
    # un, m2… sem regra -> 0 (requer conversão via Conv.Mat; implemente se tiver tabela)
    return 0.0

def calcular_item(item) -> dict:
    """
    Reproduz a lógica por linha da planilha:
    - M (energia material), R (transporte), V (equipamentos), Y (desperdício), AA (transporte do descarte)
    - Totais AB/AC e emissões (AJ/AI/AG) + co2_total_kg (soma dos canais)
    """
    Material = _get_model("Material")
    Insumo = _get_model("Insumo")

    # parâmetros globais
    HP_TO_W = obter_parametro("HP_TO_W", 745.7)
    EMISSAO_KGCO2_POR_GJ = obter_parametro("EMISSAO_KGCO2_POR_GJ", 74.1)
    KCAL_TO_MJ = obter_parametro("KCAL_TO_MJ", 0.004184)  # não usado diretamente aqui

    # fatores de transporte (Transp - MO)
    E10 = obter_fator_transporte("E10", 0.0)  # MJ/(kg·km) - transporte do item
    E11 = obter_fator_transporte("E11", 0.0)  # MJ/(kg·km) - transporte do descarte

    # material do insumo
    dens = 0.0
    energia_mj_kg = fator_L = fator_E = fator_F = coef_O = divisor_P = 0.0
    if item.insumo_id:
        ins = Insumo.objects.select_related("material").filter(id=item.insumo_id).first()
        mat = ins.material if ins else None
        if mat:
            dens = float(mat.densidade_kg_m3 or 0.0)
            energia_mj_kg = float(mat.energia_mj_kg or 0.0)
            fator_L = float(mat.fator_comp_L or 1.0)
            fator_E = float(mat.fator_emissao_material_E or 0.0)
            fator_F = float(mat.fator_emissao_total_F or 0.0)
            coef_O = float(mat.coef_transporte_O or 1.0)
            divisor_P = float(mat.divisor_para_massa_P or 0.0)

    # massa equivalente (kg)
    q_kg = normalizar_para_kg(item.quantidade or 0.0, item.unidade, dens)

    # energia base K e composição L -> M
    K = q_kg * energia_mj_kg  # se houver "Conv. Mat", aplique fator aqui (extensível)
    L = fator_L if fator_L else 1.0
    M = K * L  # energia do material

    # massa Q: algumas fórmulas usam K/P; se não houver P, use q_kg
    Q = (K / divisor_P) if divisor_P else q_kg

    # transporte do item (R)
    dist = float(item.distancia_km or 0.0)
    R = E10 * (coef_O if coef_O else 1.0) * Q * max(dist, 0.0)

    # equipamentos (V)
    pot_w = float(item.potencia_w or 0.0)
    tempo_h = float(item.tempo_uso_h or 0.0)
    V = pot_w * tempo_h * 3600.0 / 1e6  # MJ

    # desperdício (Y, AA)
    X = item.percentual_desperdicio
    if X is None:
        material_id = item.insumo.material_id if item.insumo_id else None
        X = desperdicio_default(material_id, item.etapa_obra)
    X = float(X or 0.0)
    Y = X * M
    Z = X * Q  # massa descartada
    AA = X * R + Z * E11 * max(dist, 0.0)

    # tot energia
    AB = M + R + V + Y + AA
    AC = AB / 1000.0

    # emissões (3 canais)
    AJ = AC * EMISSAO_KGCO2_POR_GJ
    AI = K * fator_E
    AG = fator_F * AB

    co2_total = AJ + AI + AG

    return {
        "q_kg": q_kg,
        "energia_material_mj": M,
        "energia_transporte_mj": R,
        "energia_equip_mj": V,
        "energia_desperdicio_mj": Y,
        "energia_transp_descarte_mj": AA,
        "energia_total_mj": AB,
        "energia_total_gj": AC,
        "co2_por_gj_kg": AJ,
        "co2_material_kg": AI,
        "co2_total_fator_kg": AG,
        "co2_total_kg": co2_total,
    }

def atualizar_totais_obra(obra):
    obra.calcular_impacto_total()
