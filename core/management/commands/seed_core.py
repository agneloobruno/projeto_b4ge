from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Estado, Cidade, ParametrosOperacionais, FatorTransporte

class Command(BaseCommand):
    help = "Popula seeds mínimas para testes"

    @transaction.atomic
    def handle(self, *args, **options):
        mt, _ = Estado.objects.get_or_create(sigla='MT', defaults={'nome': 'Mato Grosso'})
        cuiaba, _ = Cidade.objects.get_or_create(estado=mt, nome='Cuiabá')

        ParametrosOperacionais.objects.get_or_create(
            nome='padrão',
            defaults=dict(
                fator_kcal_por_hora_pessoa=250,
                pessoas_por_equipe=3,
                horas_por_dia=8,
                fator_kgCO2e_por_GJ=74.1,
                fator_kgCO2e_eletricidade_por_GJ=63.1,
            )
        )

        FatorTransporte.objects.get_or_create(
            nome='rodoviario_padrao',
            defaults=dict(
                energia_MJ_por_t_km=1.0,
                co2e_kg_por_t_km=0.07,
            )
        )

        self.stdout.write(self.style.SUCCESS('Seeds criadas/atualizadas.'))
