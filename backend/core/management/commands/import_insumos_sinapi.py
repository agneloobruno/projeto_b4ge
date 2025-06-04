from django.core.management.base import BaseCommand
from core.models import Material, Insumo
import pandas as pd
import os
import unicodedata
import csv

class Command(BaseCommand):
    help = "Importa dados de insumos SINAPI e vincula aos materiais existentes (por correspondência parcial)"

    def normalize(self, text):
        # Remove acentos, pontuações, espaços extras e coloca em maiúsculas
        if not isinstance(text, str):
            return ""
        text = unicodedata.normalize("NFKD", text).encode("ASCII", "ignore").decode("utf-8")
        return text.upper().strip()

    def handle(self, *args, **kwargs):
        file_path = os.path.join(os.getcwd(), "data", "SINAPI_Preco_Ref_Insumos_MT_202412_Desonerado.xlsx")
        if not os.path.isfile(file_path):
            self.stdout.write(self.style.ERROR(f"❌ Arquivo não encontrado: {file_path}"))
            return

        df = pd.read_excel(file_path)
        print("📄 Colunas detectadas na planilha:")
        print(df.columns.tolist())

        # Normaliza os nomes das colunas
        df.columns = df.columns.str.strip().str.upper()

        df = df.rename(columns={
            "CODIGO": "codigo",
            "DESCRICAO DO INSUMO": "descricao",
            "UNIDADE DE MEDIDA": "unidade"
        })

        materiais_queryset = Material.objects.all()
        materiais = [(m.id, self.normalize(m.descricao), m.descricao) for m in materiais_queryset]

        total = 0
        vinculados = 0
        nao_encontrados = []

        for _, row in df.iterrows():
            cod = str(row["codigo"]).strip()
            desc = str(row["descricao"]).strip()
            unidade = str(row["unidade"]).strip()

            desc_normalizado = self.normalize(desc)
            material_encontrado = None

            for material_id, material_normalizado, original_desc in materiais:
                if material_normalizado in desc_normalizado:
                    material_encontrado = (material_id, original_desc)
                    break

            if material_encontrado:
                material_id, material_desc = material_encontrado
                material_obj = Material.objects.get(id=material_id)

                insumo, created = Insumo.objects.get_or_create(
                    codigo_sinapi=cod,
                    defaults={
                        "descricao": desc,
                        "unidade": unidade,
                        "material": material_obj
                    }
                )
                self.stdout.write(f"🔗 Vinculado: {desc} → {material_desc}")
                vinculados += 1
            else:
                nao_encontrados.append(desc)

            total += 1

        # Relatórios
        self.stdout.write(self.style.SUCCESS(f"✅ {vinculados} insumos vinculados a materiais."))
        self.stdout.write(f"🔍 Total de linhas processadas: {total}")

        if nao_encontrados:
            self.stdout.write(self.style.WARNING(f"⚠️ {len(nao_encontrados)} insumos não foram vinculados."))

            # Exporta para CSV
            csv_path = os.path.join(os.getcwd(), "insumos_nao_vinculados.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["descricao"])
                for linha in nao_encontrados:
                    writer.writerow([linha])
            self.stdout.write(f"📁 Exportado para: {csv_path}")
