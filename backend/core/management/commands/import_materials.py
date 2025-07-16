from django.core.management.base import BaseCommand
from core.models import Material, Cidade, DistanciaInsumoCidade
import pandas as pd
import os
import unicodedata
import csv

class Command(BaseCommand):
    help = "Importa dados de materiais com características ambientais e distância para Cuiabá"

    def normalize(self, text):
        if not isinstance(text, str):
            return ""
        text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
        return text.upper().strip()

    def safe_str(self, value):
        return str(value).strip() if pd.notna(value) else None

    def safe_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def safe_int(self, value):
        try:
            return int(float(value))  # trata 25000.0
        except (TypeError, ValueError):
            return None

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), "data", "Banco_Materiais.xlsx")
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f"❌ Arquivo não encontrado: {file_path}"))
            return

        try:
            df = pd.read_excel(file_path)
            df.columns = df.columns.str.strip().str.upper()
            df = df.loc[:, ~df.columns.str.contains('^UNNAMED')]
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Erro ao carregar planilha: {e}"))
            return

        df = df.rename(columns={
            'DESCRIÇÃO': 'DESCRICAO',
            'DENSIDADE (KG/M3)': 'DENSIDADE',
            'ENERGIA EMBUTIDA (MJ/KG)': 'ENERGIA_KG',
            'ENERGIA EMBUTIDA (MJ/M3)': 'ENERGIA_M3',
            'KGCO2EQ/KG': 'CO2_KG',
            'FATOR DE ACRÉSCIMO PARA MANUTENÇÃO (REF. 50 ANOS) (TAVARES)': 'FATOR_MANUTENCAO',
            'REFERÊNCIA': 'REFERENCIA',
            'DISTÂNCIA DE TRANSPORTE (KM)': 'DISTANCIA_KM',
            'CAPACIDADE DO CAMINHÃO (KG)': 'CAPACIDADE_CAMINHAO',
            'REFERÊNCIA PARA CUIABÁ': 'REFERENCIA_CUIABA'
        })

        total = 0
        salvos = 0
        erros = []

        for _, row in df.iterrows():
            try:
                descricao_raw = row.get('DESCRICAO')
                if pd.isna(descricao_raw) or not str(descricao_raw).strip():
                    continue

                descricao = str(descricao_raw).strip()

                material, _ = Material.objects.update_or_create(
                    descricao=descricao,  # usado apenas como filtro
                    defaults={
                        'densidade': self.safe_float(row.get('DENSIDADE')),
                        'energia_embutida_mj_kg': self.safe_float(row.get('ENERGIA_KG')),
                        'energia_embutida_mj_m3': self.safe_float(row.get('ENERGIA_M3')),
                        'co2_kg': self.safe_float(row.get('CO2_KG')),
                        'fator_manutencao': self.safe_float(row.get('FATOR_MANUTENCAO')),
                        'referencia': self.safe_str(row.get('REFERENCIA')),
                        'capacidade_caminhao': self.safe_int(row.get('CAPACIDADE_CAMINHAO'))
                    }
                )

                nome_cidade = self.safe_str(row.get('REFERENCIA_CUIABA'))
                if nome_cidade:
                    cidade, _ = Cidade.objects.get_or_create(nome=nome_cidade)
                    distancia = self.safe_float(row.get('DISTANCIA_KM'))
                    DistanciaInsumoCidade.objects.update_or_create(
                        cidade=cidade,
                        material=material,
                        defaults={'km': distancia}
                    )

                self.stdout.write(f"✅ Importado: {descricao}")
                salvos += 1
            except Exception as e:
                erros.append((str(row.get('DESCRICAO')), str(e)))

            total += 1

        self.stdout.write(self.style.SUCCESS(f"🎯 {salvos} materiais importados com sucesso de {total} linhas."))

        if erros:
            erro_path = os.path.join(os.getcwd(), "materiais_erro.csv")
            with open(erro_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["descricao", "erro"])
                for linha in erros:
                    writer.writerow(linha)
            self.stdout.write(self.style.WARNING(f"⚠️ {len(erros)} materiais com erro. Exportado para: {erro_path}"))
