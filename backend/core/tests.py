from django.test import TestCase
from core.models import Obra

class ObraTestCase(TestCase):
    def test_criacao_obra(self):
        obra = Obra.objects.create(
            nome="Teste Residencial",
            tipologia="Residencial",
            estado="MT",
            cidade="Cuiabá",
            area_total_construir=120.5
        )
        self.assertEqual(obra.nome, "Teste Residencial")
        self.assertEqual(obra.tipologia, "Residencial")
        self.assertEqual(obra.estado, "MT")
        self.assertEqual(obra.cidade, "Cuiabá")
        self.assertAlmostEqual(obra.area_total_construir, 120.5)
