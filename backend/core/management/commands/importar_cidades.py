import csv
from django.core.management.base import BaseCommand
from core.models import Estado, Cidade


class Command(BaseCommand):
    help = 'Importa estados e cidades a partir dos arquivos CSV'

    def handle(self, *args, **kwargs):
        Estado.objects.all().delete()
        Cidade.objects.all().delete()

        estados_map = {}

        # Importa estados
        with open('data/estados.csv', newline='', encoding='utf-8') as estados_file:
            reader = csv.reader(estados_file)
            headers = next(reader)
            headers = [h.encode('utf-8').decode('utf-8-sig').strip().lower().replace(" ", "_") for h in headers]

            for row in reader:
                row_data = dict(zip(headers, row))
                estado = Estado.objects.create(
                    codigo=int(row_data['codigo_uf']),
                    sigla=row_data['uf'],
                    nome=row_data['nome'],
                    latitude=float(row_data['latitude']),
                    longitude=float(row_data['longitude']),
                    regiao=row_data['regiao']
                )
                estados_map[int(row_data['codigo_uf'])] = estado

        # Importa cidades
        with open('data/municipios.csv', newline='', encoding='utf-8') as municipios_file:
            reader = csv.reader(municipios_file)
            headers = next(reader)
            headers = [h.encode('utf-8').decode('utf-8-sig').strip().lower().replace(" ", "_") for h in headers]

            for row in reader:
                row_data = dict(zip(headers, row))
                codigo_uf = int(row_data['cod_uf'])
                nome = row_data['nome']
                estado = estados_map.get(codigo_uf)
                if estado:
                    Cidade.objects.create(nome=nome, estado=estado)

        self.stdout.write(self.style.SUCCESS('✅ Estados e cidades importados com sucesso!'))
