from core.models import Composicao, ItemDeComposicao

def calcular_impacto(composicao: Composicao, multiplicador=1.0, nivel=0, visitados=None) -> dict:
    """
    Calcula o impacto ambiental de uma composição de forma recursiva.
    Ignora ciclos e itens marcados como inválidos.
    """
    if visitados is None:
        visitados = set()

    if composicao.pk in visitados:
        print(f"⚠️ Ciclo detectado na composição {composicao.codigo}, ignorando para evitar recursão infinita.")
        return {"energia_mj": 0, "energia_gj": 0, "co2_kg": 0}

    visitados.add(composicao.pk)

    total_mj = 0
    total_co2 = 0

    for item in composicao.itens.filter(valido=True):  # ✅ Ignora itens problemáticos
        fator = item.proporcao or 0

        if item.insumo:
            material = item.insumo.material
            if material:
                fator_manut = material.fator_manutencao or 1
                energia_mj = (material.energia_embutida_mj_kg or 0) * fator * fator_manut
                co2_kg = (material.co2_kg or 0) * fator * fator_manut

                total_mj += energia_mj * multiplicador
                total_co2 += co2_kg * multiplicador

        elif item.subcomposicao and item.subcomposicao.pk != composicao.pk:
            sub_resultado = calcular_impacto(
                item.subcomposicao,
                multiplicador=fator * multiplicador,
                nivel=nivel + 1,
                visitados=visitados.copy()  # copia para evitar interferência entre ramos
            )
            total_mj += sub_resultado["energia_mj"]
            total_co2 += sub_resultado["co2_kg"]

    return {
        "energia_mj": round(total_mj, 4),
        "energia_gj": round(total_mj / 1000, 4),
        "co2_kg": round(total_co2, 4),
    }
