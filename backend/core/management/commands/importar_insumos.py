from django.core.management.base import BaseCommand
from core.models import Material, Insumo
import pandas as pd
import os
import unicodedata
import csv

class Command(BaseCommand):
    help = "Importa insumos do SINAPI e tenta vincular automaticamente ao Material existente"

    def normalize(self, text):
        # Remove acentos, espaços, pontuação e põe em maiúsculas
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
        df.columns = df.columns.str.strip().str.upper()
        df = df.rename(columns={
            "CODIGO": "CODIGO",
            "DESCRICAO DO INSUMO": "DESCRICAO",
            "UNIDADE DE MEDIDA": "UNIDADE"
        })

        materiais = list(Material.objects.all())
        total = 0
        vinculados = 0
        nao_vinculados = []

        for _, row in df.iterrows():
            codigo = str(row["CODIGO"]).strip()
            descricao = str(row["DESCRICAO"]).strip()
            unidade = str(row["UNIDADE"]).strip()
            desc_normalizado = self.normalize(descricao)

            material_encontrado = None
            for m in materiais:
                if self.normalize(m.descricao) in desc_normalizado:
                    material_encontrado = m
                    break

            if material_encontrado:
                insumo, created = Insumo.objects.get_or_create(
                    codigo_sinapi=codigo,
                    defaults={
                        "descricao": descricao,
                        "unidade": unidade,
                        "material": material_encontrado
                    }
                )
                self.stdout.write(f"🔗 Vinculado: {descricao} → {material_encontrado.descricao}")
                vinculados += 1
            else:
                nao_vinculados.append(descricao)


            if material_encontrado:
                self.stdout.write(f"🔗 Vinculado: {descricao} → {material_encontrado.descricao}")
                vinculados += 1
            else:
                nao_vinculados.append(descricao)

            total += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {vinculados} insumos vinculados a materiais."))
        self.stdout.write(f"🔍 Total de linhas processadas: {total}")

        if nao_vinculados:
            csv_path = os.path.join(os.getcwd(), "insumos_nao_vinculados.csv")
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["descricao"])
                for d in nao_vinculados:
                    writer.writerow([d])
            self.stdout.write(self.style.WARNING(f"⚠️ {len(nao_vinculados)} insumos não foram vinculados. Exportado para: {csv_path}"))
