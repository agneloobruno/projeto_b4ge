from .models import InsumoAplicado, Material, DistanciaInsumoCidade
from .utils import calcular_impacto

def atualizar_impacto_obra(obra):
    """
    Remove os InsumoAplicado existentes e gera novos a partir das composições
    associadas à obra. Calcula impacto ambiental (energia, transporte, CO2).
    """
    # Remove todos os itens aplicados existentes
    obra.itens_aplicados.all().delete()

    for etapa in obra.etapas_tecnicas.all():
        dados = etapa.dados
        composicoes_codigos = dados.get("composicoes", [])

        for cod in composicoes_codigos:
            from core.models import Composicao  # Import local para evitar import circular
            try:
                composicao = Composicao.objects.get(codigo=cod)
            except Composicao.DoesNotExist:
                continue

            impacto = calcular_impacto(composicao)

            # Cria registro para a composição
            InsumoAplicado.objects.create(
                obra=obra,
                tipo="COMPOSICAO",
                etapa_obra=etapa.nome,
                composicao=composicao,
                unidade=composicao.unidade,
                energia_embutida_mj=impacto["energia_mj"],
                energia_embutida_gj=impacto["energia_gj"],
                co2_kg=impacto["co2_kg"]
            )

            # Cria registros para cada insumo da composição
            for item in composicao.itens.filter(valido=True):
                if item.insumo and item.insumo.material:
                    material = item.insumo.material
                    fator_manut = material.fator_manutencao or 1
                    energia = (material.energia_embutida_mj_kg or 0) * (item.proporcao or 0) * fator_manut
                    co2 = (material.co2_kg or 0) * (item.proporcao or 0) * fator_manut

                    # Cálculo de transporte (cidade da obra ↔ material)
                    distancia = 0
                    try:
                        dt = DistanciaInsumoCidade.objects.get(insumo=item.insumo, cidade_da_obra=obra.cidade)
                        distancia = dt.distancia
                    except DistanciaInsumoCidade.DoesNotExist:
                        pass  # Se não encontrar a distância, considera como 0

                    # Considera apenas se a distância for maior que 0
                    if distancia > 0:
                        # Calcula impacto de transporte (considerando ida e volta)
                        impacto_transporte = 2 * distancia * (material.peso_kg or 0) * (material.co2_kg or 0)
                        co2 += impacto_transporte

                    # Atualiza ou cria registro do insumo aplicado
                    InsumoAplicado.objects.update_or_create(
                        obra=obra,
                        tipo="INSUMO",
                        etapa_obra=etapa.nome,
                        insumo=item.insumo,
                        defaults={
                            "unidade": material.unidade,
                            "energia_embutida_mj": energia,
                            "energia_embutida_gj": energia / 1000,
                            "co2_kg": co2
                        }
                    )

    # Recalcula o impacto total da obra
    obra.calcular_impacto_total()