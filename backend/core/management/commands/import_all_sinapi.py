from django.core.management.base import BaseCommand
from core.models import Composicao, ComposicaoItem, Material
import pandas as pd
import os

class Command(BaseCommand):
    help = "Importa dados completos do SINAPI (composições, itens e insumos)"

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(base_dir):
            self.stdout.write(self.style.ERROR("❌ Pasta 'data' não encontrada."))
            return

        # Caminhos esperados
        analitico_path = os.path.join(base_dir, "SINAPI_Custo_Ref_Composicoes_Analitico_MT_202412_Desonerado.xlsx")
        sintetico_path = os.path.join(base_dir, "SINAPI_Custo_Ref_Composicoes_Sintetico_MT_202412_Desonerado.xlsx")
        insumos_path = os.path.join(base_dir, "SINAPI_Preco_Ref_Insumos_MT_202412_Desonerado.xlsx")
        familia_path = os.path.join(base_dir, "_SINAPI_Relatório_Família_de_Insumos_2024_12.xlsx")

        # Validação de arquivos
        for path in [analitico_path, sintetico_path, insumos_path, familia_path]:
            if not os.path.isfile(path):
                self.stdout.write(self.style.ERROR(f"❌ Arquivo não encontrado: {path}"))
                return

        # --- Importa Composições Analíticas ---
        df = pd.read_excel(analitico_path)
        df = df.rename(columns={
            "CODIGO DA COMPOSICAO": "codigo_composicao",
            "DESCRICAO DA COMPOSICAO": "descricao_composicao",
            "UNIDADE": "unidade_composicao",
            "CODIGO ITEM": "codigo_item",
            "DESCRIÇÃO ITEM": "descricao_item",
            "UNIDADE ITEM": "unidade_item",
            "COEFICIENTE": "coeficiente"
        })

        df_validas = df.dropna(subset=["codigo_composicao", "codigo_item", "coeficiente"])
        self.stdout.write(f"📊 Linhas válidas (analítico): {len(df_validas)}")

        composicoes_criadas = {}
        itens_criados = 0

        for _, row in df_validas.iterrows():
            cod = str(row["codigo_composicao"]).strip()
            desc = str(row["descricao_composicao"]).strip()
            unidade = str(row["unidade_composicao"]).strip()

            composicao, _ = Composicao.objects.get_or_create(
                codigo=cod,
                defaults={"descricao": desc, "unidade": unidade}
            )
            composicoes_criadas[cod] = composicao

            try:
                material = Material.objects.get(descricao__iexact=row["descricao_item"].strip())
                ComposicaoItem.objects.create(
                    composicao_pai=composicao,
                    material=material,
                    unidade=row["unidade_item"],
                    proporcao=row["coeficiente"]
                )
                itens_criados += 1
            except Material.DoesNotExist:
                continue

        self.stdout.write(self.style.SUCCESS(f"✅ {len(composicoes_criadas)} composições criadas."))
        self.stdout.write(self.style.SUCCESS(f"✅ {itens_criados} itens de composição vinculados."))

        # (Opcional) Etapas futuras: 
        # - Preencher valores da composição com base na planilha sintética
        # - Atualizar preços dos materiais com base na planilha de insumos
        # - Considerar vínculos da planilha de família de insumos (ainda não implementado)

        self.stdout.write(self.style.WARNING("⚠️ Importações auxiliares (sintética, insumos, vínculos) ainda não foram processadas."))
