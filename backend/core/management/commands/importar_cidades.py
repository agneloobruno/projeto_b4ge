# importar_estados_cidades.py

import csv
from django.core.management.base import BaseCommand
from core.models import Estado, Cidade  # ajuste conforme seu app

class Command(BaseCommand):
    help = 'Importa estados e cidades a partir dos arquivos CSV'

    def handle(self, *args, **kwargs):
        Estado.objects.all().delete()
        Cidade.objects.all().delete()

        with open('data/estados.csv', newline='', encoding='utf-8') as estados_file:
            reader = csv.DictReader(estados_file)
            estados_map = {}
            for row in reader:
                estado = Estado.objects.create(
                    codigo=int(row['codigo_uf']),
                    sigla=row['uf'],
                    nome=row['nome'],
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    regiao=row['regiao']
                )
                estados_map[int(row['codigo_uf'])] = estado

        with open('data/municipios.csv', newline='', encoding='utf-8') as municipios_file:
            reader = csv.DictReader(municipios_file)
            for row in reader:
                codigo_uf = int(row['COD UF'])
                nome = row['NOME']
                estado = estados_map.get(codigo_uf)
                if estado:
                    Cidade.objects.create(nome=nome, estado=estado)

        self.stdout.write(self.style.SUCCESS('✅ Estados e cidades importados com sucesso!'))
