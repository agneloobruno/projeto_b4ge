from django.core.management.base import BaseCommand
from core.models import Composicao, ItemDeComposicao, Insumo
import pandas as pd
import os

class Command(BaseCommand):
    help = "Importa ItemDeComposicao com base na planilha adaptada da aba LISTA (B4GE)"

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), "data", "Lista.xlsx")
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR("❌ Arquivo Pasta1.xlsx não encontrado na pasta /data"))
            return

        df = pd.read_excel(file_path)
        df.columns = [col.strip() for col in df.columns]

        criados = 0
        ignorados = 0

        for _, row in df.iterrows():
            cod_comp = str(row["Cód. SINAPI"]).strip()
            desc_item = str(row["Descrição"]).strip()
            unidade = str(row["Unidade"]).strip()
            proporcao = row["Proporção"]

            if pd.isna(cod_comp) or pd.isna(desc_item) or pd.isna(proporcao):
                ignorados += 1
                continue

            try:
                composicao = Composicao.objects.get(codigo=cod_comp)
            except Composicao.DoesNotExist:
                self.stdout.write(f"⚠️ Composição não encontrada: {cod_comp}")
                ignorados += 1
                continue

            try:
                insumo = Insumo.objects.get(descricao__iexact=desc_item)
            except Insumo.DoesNotExist:
                self.stdout.write(f"⚠️ Insumo não encontrado: {desc_item}")
                ignorados += 1
                continue

            proporcao = float(str(proporcao).replace(",", "."))

            ItemDeComposicao.objects.create(
                composicao_pai=composicao,
                insumo=insumo,
                unidade=unidade,
                proporcao=proporcao
            )
            criados += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {criados} itens de composição importados com sucesso."))
        self.stdout.write(self.style.WARNING(f"⚠️ {ignorados} linhas foram ignoradas por falta de dados ou inconsistências."))
