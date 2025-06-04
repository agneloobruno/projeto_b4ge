from django.core.management.base import BaseCommand
from core.models import Composicao, ComposicaoItem, Material
import pandas as pd
import os

class Command(BaseCommand):
    help = "Importa ComposicaoItem a partir da planilha 'Lista' da B4GE"

    def handle(self, *args, **kwargs):
        file_path = os.path.join("data", "Pasta1.xlsx")
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR("❌ Arquivo Pasta1.xlsx não encontrado em /data"))
            return

        df = pd.read_excel(file_path)
        df = df.rename(columns={
            "Cód. SINAPI": "codigo_composicao",
            "Descrição": "descricao",
            "Unidade": "unidade",
            "Proporção": "proporcao",
            "Quantidade": "quantidade",
            " Carbono Embutido dos Materiais (kgCO2/kg)": "co2_kg",
            "Energia embutida (MJ/kg)": "energia_embutida_mj_kg",
            "Fator manutenção": "fator_manutencao",
        })

        df = df.dropna(subset=["codigo_composicao", "descricao", "proporcao"])
        criados = 0
        for _, row in df.iterrows():
            cod = str(row["codigo_composicao"]).strip()
            try:
                composicao = Composicao.objects.get(codigo=cod)
            except Composicao.DoesNotExist:
                continue

            try:
                material = Material.objects.get(descricao__iexact=row["descricao"].strip())
            except Material.DoesNotExist:
                continue

            proporcao = float(str(row["proporcao"]).replace(",", "."))
            quantidade = float(str(row.get("quantidade", 0)).replace(",", ".") or 0)
            energia_mj = proporcao * float(row.get("energia_embutida_mj_kg") or 0)
            co2_total = proporcao * float(row.get("co2_kg") or 0)

            ComposicaoItem.objects.create(
                composicao_pai=composicao,
                material=material,
                unidade=row.get("unidade", "kg"),
                proporcao=proporcao,
                quantidade=quantidade,
                energia_embutida_mj=energia_mj,
                energia_embutida_gj=energia_mj / 1000,
                co2_kg=co2_total
            )
            criados += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {criados} itens de composição vinculados com sucesso."))
