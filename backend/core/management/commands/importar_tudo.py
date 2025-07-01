# backend/core/management/commands/importar_tudo.py
import os
import pandas as pd
import json
from django.core.management.base import BaseCommand
from core.models import Material, Insumo, Composicao, ItemDeComposicao
from django.db import transaction

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = '/app/data'

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

        total_novos = 0
        total_atualizados = 0
        for _, row in df.iterrows():
            obj, created = Material.objects.update_or_create(
                descricao=row['Descrição'],
                defaults={
                    'densidade': row.get('Densidade (kg/m3)'),
                    'energia_embutida_mj_kg': row.get('Energia Embutida (MJ/KG)'),
                    'energia_embutida_mj_m3': row.get('Energia Embutida (MJ/M3)'),
                    'co2_kg': row.get('kgCO2eq/kg'),
                    'fator_manutencao': row.get('Fator de acréscimo para manutenção (ref. 50 anos) (Tavares)'),
                    'referencia': row.get('Referência'),
#                    'distancia_transporte': row.get('Distância de transporte (km)'),
                    'capacidade_caminhao': row.get('Capacidade do Caminhão (KG)'),
                    'referencia_para_cuiaba': row.get('Referência para Cuiabá')
                }
            )
            if created:
                total_novos += 1
            else:
                total_atualizados += 1
        self.stdout.write(f"✔️ Materiais: {total_novos} criados, {total_atualizados} atualizados")

    def importar_insumos(self):
        path = os.path.join(DATA_DIR, "SINAPI_Preco_Ref_Insumos_MT_202412_Desonerado.xlsx")
        df = pd.read_excel(path)

        total_criados = 0
        total_atualizados = 0
        ignorados = 0
        for _, row in df.iterrows():
            mat = Material.objects.filter(descricao__icontains=row['descricao'].strip()).first()
            if not mat:
                self.stdout.write(self.style.WARNING(f"⚠️ Material não encontrado para insumo: {row['descricao']}"))
                ignorados += 1
                continue
            obj, created = Insumo.objects.update_or_create(
                codigo_sinapi=row['codigo'],
                defaults={
                    'descricao': row['descricao'],
                    'unidade': row['unidade'],
                    'material': mat
                }
            )
            if created:
                total_criados += 1
            else:
                total_atualizados += 1
        self.stdout.write(f"✔️ Insumos: {total_criados} criados, {total_atualizados} atualizados, {ignorados} ignorados")

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
            if isinstance(itens, str):
                try:
                    itens = json.loads(itens)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"⚠️ Erro ao carregar itens da composição {comp.codigo}: {e}"))
                    continue

            if not isinstance(itens, list):
                continue

            for item in itens:
                insumo = Insumo.objects.filter(codigo_sinapi=item.get('codigo')).first()
                if not insumo:
                    self.stdout.write(self.style.WARNING(f"⚠️ Insumo não encontrado para item: {item}"))
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
