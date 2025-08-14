from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal

from core.models import (
    Estado, Cidade, Material, ConversaoMaterial,
    Composicao, ItemDeComposicao, DistanciaInsumoCidade,
    EtapaConstrutiva
)

class Command(BaseCommand):
    help = "Cria dados de demonstração mínimos para testar /impactos"

    @transaction.atomic
    def handle(self, *args, **opts):
        # Localidade já criada em seed_core; só assegurando:
        mt, _ = Estado.objects.get_or_create(sigla='MT', defaults={'nome': 'Mato Grosso'})
        cuiaba, _ = Cidade.objects.get_or_create(estado=mt, nome='Cuiabá')

        # 1) Material base
        concreto, _ = Material.objects.get_or_create(
            nome='Concreto fck25',
            defaults=dict(
                unidade_base='kg',
                densidade_kg_m3=Decimal('2400'),
                energia_MJ_por_kg=Decimal('1.20'),
                co2e_kg_por_kg=Decimal('0.12'),
            )
        )

        # (exemplo de conversão m2->kg para 0,10 m de espessura)
        ConversaoMaterial.objects.get_or_create(
            material=concreto,
            origem_unidade='m2',
            destino_unidade='kg',
            espessura_m=Decimal('0.10'),
            defaults=dict(fator_massa_kg_por_origem=Decimal('240.0'))  # 2.400 kg/m3 * 0,10 m = 240 kg por m2
        )

        # 2) Distância de transporte p/ Cuiabá
        DistanciaInsumoCidade.objects.get_or_create(
            material=concreto, cidade=cuiaba,
            defaults=dict(distancia_km=Decimal('50'))
        )

        # 3) Composição + Item (etapa: estrutura)
        comp, _ = Composicao.objects.get_or_create(
            codigo='EST-001',
            defaults=dict(nome='Estrutura de Concreto', etapa=EtapaConstrutiva.ESTRUTURA)
        )

        # Item de 1000 kg de concreto (com 5% de desperdício)
        ItemDeComposicao.objects.get_or_create(
            composicao=comp,
            material=concreto,
            unidade_medida='kg',
            quantidade=Decimal('1000'),
            defaults=dict(desperdicio_pct=Decimal('5.0'))
        )

        self.stdout.write(self.style.SUCCESS('Seed DEMO criada/atualizada.'))
