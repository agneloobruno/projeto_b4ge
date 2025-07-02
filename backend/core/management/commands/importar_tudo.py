import os
import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Material, Insumo, Composicao, ItemDeComposicao
from django.db import transaction

DATA_DIR = "backend/data"

class Command(BaseCommand):
    help = 'Importa todos os dados (materiais, insumos, composições) a partir dos arquivos em backend/data'

    def handle(self, *args, **options):
        self.stdout.write("🚀 Iniciando importação de dados...")
        with transaction.atomic():
            self.importar_materiais()
            self.importar_insumos()
            self.importar_composicoes()
        self.stdout.write(self.style.SUCCESS("✅ Importação concluída com sucesso."))

    def importar_materiais(self):
        path = os.path.join(DATA_DIR, "banco_materiais.xlsx")
        df = pd.read_excel(path)

        total = 0
        for _, row in df.iterrows():
            mat, created = Material.objects.update_or_create(
                descricao=row['descricao'],
                defaults={
                    'densidade': row.get('densidade'),
                    'energia_embutida_mj_kg': row.get('energia_embutida_mj_kg'),
                    'energia_embutida_mj_m3': row.get('energia_embutida_mj_m3'),
                    'co2_kg': row.get('co2_kg'),
                    'fator_manutencao': row.get('fator_manutencao'),
                    'referencia': row.get('referencia'),
                    'capacidade_caminhao': row.get('capacidade_caminhao'),
                    'referencia_para_cuiaba': row.get('referencia_para_cuiaba')
                }
            )
            if created:
                total += 1
        self.stdout.write(f"✔️ Materiais importados: {total}")

    def importar_insumos(self):
        path = os.path.join(DATA_DIR, "SINAPI_Preco_Ref_Insumos_MT_202412_Desonerado.xlsx")
        df = pd.read_excel(path)

        total = 0
        for _, row in df.iterrows():
            mat = Material.objects.filter(descricao__icontains=row['descricao'].strip()).first()
            if not mat:
                continue
            ins, created = Insumo.objects.update_or_create(
                codigo_sinapi=row['codigo'],
                defaults={
                    'descricao': row['descricao'],
                    'unidade': row['unidade'],
                    'material': mat
                }
            )
            if created:
                total += 1
        self.stdout.write(f"✔️ Insumos importados: {total}")

    def importar_composicoes(self):
        path = os.path.join(DATA_DIR, "SINAPI_Custo_Ref_Composicoes_Analitico_MT_202412_Desonerado.xlsx")
        df = pd.read_excel(path)

        total_composicoes = 0
        total_itens = 0

        for _, row in df.iterrows():
            comp, _ = Composicao.objects.update_or_create(
                codigo=row['codigo'],
                defaults={
                    'descricao': row['descricao'],
                    'unidade': row['unidade']
                }
            )
            total_composicoes += 1

            itens = row.get('itens')
            if not itens:
                continue

            for item in itens:
                insumo = Insumo.objects.filter(codigo_sinapi=item['codigo']).first()
                if not insumo:
                    continue
                ItemDeComposicao.objects.update_or_create(
                    composicao_pai=comp,
                    insumo=insumo,
                    defaults={
                        'unidade': item.get('unidade'),
                        'proporcao': item.get('proporcao', 1),
                        'valido': True
                    }
                )
                total_itens += 1

        self.stdout.write(f"✔️ Composições importadas: {total_composicoes}")
        self.stdout.write(f"├─ Itens de composição: {total_itens}")
