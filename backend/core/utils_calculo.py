from .models import InsumoAplicado, Material, DistanciaInsumoCidade, Obra
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

        # 🆕 Aplicar composição da fundação automaticamente, se tipologia estiver definida
        if etapa.nome.lower() == "fundação":
            tipo = obra.tipologia_fundacao
            espessura = obra.espessura_fundacao_cm
            area = obra.area_fundacao_m2

            if tipo and espessura and area:
                # Exemplo: buscar composição "Radier 15cm" por nome
                composicao_fundacao = Composicao.objects.filter(
                    descricao__icontains=tipo,
                    descricao__icontains=f"{espessura}cm"
                ).first()

                if composicao_fundacao:
                    impacto_unitario = calcular_impacto(composicao_fundacao)

                    # Aplica proporção baseada na área
                    energia_mj = impacto_unitario["energia_mj"] * area
                    energia_gj = energia_mj / 1000
                    co2_kg = impacto_unitario["co2_kg"] * area

                    InsumoAplicado.objects.create(
                        obra=obra,
                        tipo="COMPOSICAO",
                        etapa_obra=etapa.nome,
                        composicao=composicao_fundacao,
                        unidade=composicao_fundacao.unidade,
                        energia_embutida_mj=energia_mj,
                        energia_embutida_gj=energia_gj,
                        co2_kg=co2_kg
                    )
                    continue

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

                    # Cálculo de transporte
                    distancia = 0
                    try:
                        dt = DistanciaInsumoCidade.objects.get(insumo=item.insumo, cidade_da_obra=obra.cidade)
                        distancia = dt.distancia
                    except DistanciaInsumoCidade.DoesNotExist:
                        pass

                    if distancia > 0:
                        impacto_transporte = 2 * distancia * (material.peso_kg or 0) * (material.co2_kg or 0)
                        co2 += impacto_transporte

                    # Atualiza ou cria o insumo aplicado
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

    obra.energia_total_mj = obra.energia_embutida_total()
    obra.co2_total_kg = obra.co2_total()
    obra.save()
    



    # Você pode mostrar os resultados, se quiser:
    print("Energia total (MJ):", obra.energia_embutida_total())
    print("CO2 total (kg):", obra.co2_total())
