from django.core.management.base import BaseCommand
from core.models import Composicao, ItemDeComposicao, Insumo
import pandas as pd
import os
import unicodedata

class Command(BaseCommand):
    help = "Importa dados da aba Lista, diferenciando SERVIÇOS, COMPOSIÇÕES e INSUMOS com base na coluna 5"

    def normalize(self, text):
        if not isinstance(text, str):
            return ""
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8").upper().strip()

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), "data", "SA_Calculadora de Energia Embutida e Emissões de CO2eq - B4Ge 01.06..25.xlsx")

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Arquivo não encontrado: {file_path}"))
            return

        df = pd.read_excel(file_path, sheet_name="Lista")
        df.columns = df.columns.str.strip().str.upper()

        composicao_pai = None
        total_linhas = 0
        itens_adicionados = 0
        erros = []

        for _, row in df.iterrows():
            try:
                cod = str(row.get("CÓD. SINAPI") or '').strip()
                descricao = str(row.get("DESCRIÇÃO") or '').strip()
                unidade = str(row.get("UNIDADE") or '').strip()
                etapa_obra = str(row.get("ETAPAS DA OBRA") or '').strip()
                proporcao = row.get("PROPORÇÃO")
                nivel_coluna_5 = row.get(df.columns[4])  # 5ª coluna visualmente

                classe1 = self.normalize(row.get("CLASSE 1"))
                classe2 = self.normalize(row.get("CLASSE 2"))

                # Se a coluna 5 está preenchida, é uma composição pai (serviço)
                if pd.notna(nivel_coluna_5) and cod:
                    composicao_pai, _ = Composicao.objects.get_or_create(
                        codigo=cod,
                        defaults={
                            "descricao": descricao,
                            "unidade": unidade,
                            "etapa_obra": etapa_obra
                        }
                    )
                    if composicao_pai.etapa_obra in [None, ""] and etapa_obra:
                        composicao_pai.etapa_obra = etapa_obra
                        composicao_pai.save()
                    continue

                # Se for linha sem proporção ou sem composição pai definida, ignorar
                if not composicao_pai or pd.isna(proporcao):
                    continue

                proporcao = float(proporcao)

                # Subcomposição
                if "COMPOSICAO" in classe1 or "COMPOSICAO" in classe2:
                    sub, _ = Composicao.objects.get_or_create(
                        codigo=cod,
                        defaults={"descricao": descricao, "unidade": unidade}
                    )
                    ItemDeComposicao.objects.update_or_create(
                        composicao_pai=composicao_pai,
                        subcomposicao=sub,
                        defaults={"proporcao": proporcao, "unidade": unidade}
                    )
                else:
                    # Insumo
                    insumo = Insumo.objects.filter(codigo_sinapi=cod).first()
                    if insumo:
                        ItemDeComposicao.objects.update_or_create(
                            composicao_pai=composicao_pai,
                            insumo=insumo,
                            defaults={"proporcao": proporcao, "unidade": unidade}
                        )
                itens_adicionados += 1
                total_linhas += 1

            except Exception as e:
                erros.append((descricao or "N/D", str(e)))

        self.stdout.write(self.style.SUCCESS(f"✅ {total_linhas} linhas processadas."))
        self.stdout.write(self.style.SUCCESS(f"📦 {itens_adicionados} itens adicionados ao banco."))

        if erros:
            self.stdout.write(self.style.WARNING(f"⚠️ {len(erros)} erros encontrados. Primeiros 5:"))
            for i, (desc, err) in enumerate(erros[:5]):
                self.stdout.write(f"❌ {i+1}. '{desc}' → {err}")
