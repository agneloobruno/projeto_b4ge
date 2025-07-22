import csv
from django.core.management.base import BaseCommand
from core.models import Cidade  # ajuste para seu app/modelo

class Command(BaseCommand):
    help = 'Importa cidades a partir de um arquivo CSV.'

    def handle(self, *args, **kwargs):
        path_csv = 'data/cidades.csv'

        # Limpa a tabela antes de importar
        Cidade.objects.all().delete()
        self.stdout.write(self.style.WARNING('Tabela Cidade limpa.'))

        with open(path_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                nome = row['nome'].strip()
                estado = row['estado'].strip().upper()

                if nome and estado:
                    Cidade.objects.create(nome=nome, estado=estado)
                    count += 1

            self.stdout.write(self.style.SUCCESS(f'{count} cidades importadas com sucesso.'))
