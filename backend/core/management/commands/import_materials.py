import csv
import os
from django.core.management.base import BaseCommand
from core.models import Material

class Command(BaseCommand):
    help = 'Importa materiais a partir de um arquivo CSV limpo.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Caminho para o arquivo CSV')

    def handle(self, *args, **options):
        csv_path = options['csv_path']
        self.stdout.write(self.style.SUCCESS(f'Arquivo CSV recebido: {csv_path}'))

        if not os.path.exists(csv_path):
            self.stderr.write(self.style.ERROR(f'Arquivo não encontrado: {csv_path}'))
            return

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                material, created = Material.objects.update_or_create(
                    descricao=row['descricao'],
                    defaults={
                        'densidade': self.parse_float(row.get('densidade')),
                        'energia_embutida_mj_kg': self.parse_float(row.get('energia_embutida_mj_kg')),
                        'energia_embutida_mj_m3': self.parse_float(row.get('energia_embutida_mj_m3')),
                        'co2_kg': self.parse_float(row.get('co2_kg')),
                        'fator_manutencao': self.parse_float(row.get('fator_manutencao')),
                        'referencia': row.get('referencia', ''),
                        'capacidade_caminhao': self.parse_int(row.get('capacidade_caminhao')),
                        'referencia_para_cuiaba': row.get('referencia_para_cuiaba', ''),
                    }
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'{count} materiais importados com sucesso.'))

    def parse_float(self, value):
        try:
            return float(value.replace(',', '.')) if value else None
        except Exception:
            return None

    def parse_int(self, value):
        try:
            return int(float(value)) if value else None
        except Exception:
            return None
