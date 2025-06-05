from django.core.management.base import BaseCommand
from core.models import Composicao, ComposicaoItem, Insumo
import pandas as pd
import os
import unicodedata

class Command(BaseCommand):
    help = "Importa composições e seus itens com base na aba Lista"

    def normalize(self, text):
        if not isinstance(text, str):
            return ""
        return unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8").upper().strip()

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), "data", "Lista.xlsx")
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f"❌ Arquivo não encontrado: {file_path}"))
            return

        try:
            df = pd.read_excel(file_path, sheet_name=0)
            df.columns = df.columns.str.strip().str.upper()
            self.stdout.write("📄 Colunas detectadas:")
            for col in df.columns:
                self.stdout.write(f"→ {col}")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao carregar a planilha: {e}"))
            return

        composicao_pai = None
        total_linhas = 0
        itens_adicionados = 0
        erros = []

        for _, row in df.iterrows():
            try:
                cod = str(row.get("CÓD. SINAPI") or "").strip()
                descricao = str(row.get("DESCRIÇÃO") or "").strip()
                unidade = str(row.get("UNIDADE") or "").strip()
                etapa_obra = str(row.get("ETAPAS DA OBRA") or "").strip()
                proporcao_raw = row.get("PROPORÇÃO")

                classe1 = self.normalize(row.get("CLASSE 1"))
                classe2 = self.normalize(row.get("CLASSE 2"))

                # Verifica se é linha de definição de nova composição (serviço)
                if cod and not pd.notna(proporcao_raw):
                    composicao_pai, _ = Composicao.objects.get_or_create(
                        codigo=cod,
                        defaults={
                            "descricao": descricao,
                            "unidade": unidade,
                            "etapa_obra": etapa_obra
                        }
                    )
                    # Atualiza etapa da obra se já existir mas estiver vazia
                    if composicao_pai.etapa_obra in [None, ""] and etapa_obra:
                        composicao_pai.etapa_obra = etapa_obra
                        composicao_pai.save()
                    continue

                if not composicao_pai or not pd.notna(proporcao_raw):
                    continue

                proporcao = float(proporcao_raw)

                if "COMPOSICAO" in classe1 or "COMPOSICAO" in classe2:
                    sub, _ = Composicao.objects.get_or_create(
                        codigo=cod,
                        defaults={"descricao": descricao, "unidade": unidade}
                    )
                    ComposicaoItem.objects.update_or_create(
                        composicao_pai=composicao_pai,
                        subcomposicao=sub,
                        defaults={
                            "proporcao": proporcao,
                            "unidade": unidade
                        }
                    )
                else:
                    insumo = Insumo.objects.filter(codigo_sinapi=cod).first()
                    if insumo:
                        ComposicaoItem.objects.update_or_create(
                            composicao_pai=composicao_pai,
                            insumo=insumo,
                            defaults={
                                "proporcao": proporcao,
                                "unidade": unidade
                            }
                        )
                itens_adicionados += 1
                total_linhas += 1

            except Exception as e:
                erros.append((descricao or "N/D", str(e)))

        self.stdout.write(self.style.SUCCESS(f"\n✅ {total_linhas} itens processados."))
        self.stdout.write(self.style.SUCCESS(f"📦 {itens_adicionados} ComposicaoItems adicionados."))

        if erros:
            self.stdout.write(self.style.WARNING(f"\n⚠️ {len(erros)} erros durante a importação. Primeiros 5 exemplos:"))
            for i, (desc, err) in enumerate(erros[:5]):
                self.stdout.write(f"❌ {i+1}. '{desc}' → {err}")
