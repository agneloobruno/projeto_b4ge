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
                cod = self.normalize(str(row.get("CÓD. SINAPI") or ''))
                descricao = str(row.get("DESCRIÇÃO") or '').strip()
                unidade = str(row.get("UNIDADE") or '').strip()
                etapa_obra = str(row.get("ETAPAS DA OBRA") or '').strip()
                proporcao_raw = row.get("PROPORÇÃO")
                nivel_coluna_5 = row.get("TIPO (INTERFACE DO USUÁRIO)")  # coluna 5
                classe1 = self.normalize(row.get("CLASSE 1"))
                classe2 = self.normalize(row.get("CLASSE 2"))

                if not cod:
                    continue  # Código é essencial

                # Identifica composição pai
                if pd.notna(nivel_coluna_5):
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

                if not composicao_pai or pd.isna(proporcao_raw):
                    continue  # Ignora linhas mal formatadas

                try:
                    proporcao = float(str(proporcao_raw).replace(",", "."))
                except (TypeError, ValueError):
                    continue  # Ignora proporções inválidas

                # É subcomposição
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
                    # É insumo
                    insumo = Insumo.objects.filter(codigo_sinapi=cod).first()
                    if not insumo:
                        try:
                            insumo = Insumo.objects.create(
                                codigo_sinapi=cod,
                                descricao=descricao or "Sem descrição",
                                unidade=unidade or "-",
                                material=None  # material agora é opcional
                            )
                            self.stdout.write(self.style.NOTICE(f"🆕 Criado insumo sem material: {cod} - {descricao}"))
                        except Exception as e:
                            erros.append((f"Insumo '{cod}'", f"Erro ao criar insumo: {e}"))
                            continue

                    ItemDeComposicao.objects.update_or_create(
                        composicao_pai=composicao_pai,
                        insumo=insumo,
                        defaults={"proporcao": proporcao, "unidade": unidade}
                    )

                itens_adicionados += 1
                total_linhas += 1

            except Exception as e:
                erros.append((descricao or "N/D", str(e)))

        self.stdout.write(self.style.SUCCESS(f"\n✅ {total_linhas} linhas processadas."))
        self.stdout.write(self.style.SUCCESS(f"📦 {itens_adicionados} itens adicionados ao banco."))

        if erros:
            self.stdout.write(self.style.WARNING(f"\n⚠️ {len(erros)} erros encontrados. Primeiros 5:"))
            for i, (desc, err) in enumerate(erros[:5]):
                self.stdout.write(self.style.WARNING(f"❌ {i+1}. '{desc}' → {err}"))
