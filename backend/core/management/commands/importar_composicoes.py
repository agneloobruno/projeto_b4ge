from django.core.management.base import BaseCommand
from core.models import Composicao, ComposicaoItem, Insumo
import pandas as pd
import os
import unicodedata

class Command(BaseCommand):
    help = "Importa composições e seus itens com base na aba Lista (estrutura SINAPI)"

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

        total_linhas = 0
        itens_adicionados = 0
        erros = []

        composicao_pai = None
        codigo_atual = None

        for _, row in df.iterrows():
            try:
                cod_sinapi = str(row.get("CÓD. SINAPI") or "").strip()
                descricao = str(row.get("DESCRIÇÃO") or "").strip()
                unidade = str(row.get("UNIDADE") or "").strip()
                classe1 = self.normalize(row.get("CLASSE 1"))
                classe2 = self.normalize(row.get("CLASSE 2"))
                proporcao_raw = row.get("PROPORÇÃO")

                # Troca de composição-pai?
                if cod_sinapi != codigo_atual:
                    composicao_pai, _ = Composicao.objects.get_or_create(
                        codigo=cod_sinapi,
                        defaults={"descricao": descricao, "unidade": unidade}
                    )
                    codigo_atual = cod_sinapi
                    continue  # Pula a linha da definição da composição

                # Linhas abaixo da composição são seus itens
                is_subcomposicao = "COMPOSICAO" in classe1 or "COMPOSICAO" in classe2

                proporcao = float(proporcao_raw) if pd.notna(proporcao_raw) and proporcao_raw != '' else None
                if proporcao is None:
                    raise ValueError("Proporção ausente")

                if is_subcomposicao:
                    sub, _ = Composicao.objects.get_or_create(
                        codigo=cod_sinapi,
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
                    insumo = Insumo.objects.filter(codigo_sinapi=cod_sinapi).first()
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

        self.stdout.write(self.style.SUCCESS(f"\n✅ {total_linhas} linhas processadas."))
        self.stdout.write(self.style.SUCCESS(f"📦 {itens_adicionados} itens adicionados a composições."))

        if erros:
            self.stdout.write(self.style.WARNING(f"\n⚠️ {len(erros)} erros durante a importação. Primeiros 5 exemplos:"))
            df_erros = pd.DataFrame(erros, columns=["descricao", "erro"])
            df_erros.to_csv("insumos_sem_proporcao.csv", index=False)
            self.stdout.write(self.style.WARNING(f"📁 Exportado para: insumos_sem_proporcao.csv"))
            for i, (desc, err) in enumerate(erros[:5]):
                self.stdout.write(f"❌ {i+1}. '{desc}' → {err}")
