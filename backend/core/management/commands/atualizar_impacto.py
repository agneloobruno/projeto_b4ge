from django.core.management.base import BaseCommand, CommandError
from core.models import Obra
from core.utils_calculo import atualizar_impacto_obra

class Command(BaseCommand):
    help = 'Atualiza os impactos ambientais (energia e CO₂) de uma obra a partir de suas composições'

    def add_arguments(self, parser):
        parser.add_argument('--obra_id', type=int, help='ID da obra que será processada')

    def handle(self, *args, **options):
        obra_id = options.get('obra_id')

        if not obra_id:
            raise CommandError("Você deve fornecer o ID da obra com --obra_id")

        try:
            obra = Obra.objects.get(id=obra_id)
        except Obra.DoesNotExist:
            raise CommandError(f"Obra com ID {obra_id} não encontrada.")

        resultado = atualizar_impacto_obra(obra)
        self.stdout.write(self.style.SUCCESS(f"✅ {resultado}"))
        self.stdout.write(self.style.SUCCESS(f"Impactos atualizados para a obra {obra.nome} (ID: {obra.id})"))
#                         defaults={
#                             'etapa_obra': etapa.nome,
#                             'composicao': composicao,
#                             'unidade': composicao.unidade,
#                             'energia_embutida_mj': energia,
#                             'energia_embutida_gj': energia / 1000,
#                             'co2_kg': co2
#                         }
#                     )
