from django.test import TestCase
from core.models import Cidade, Obra, Composicao, ItemDeComposicao, Material, Insumo, EtapaConstrutiva, DistanciaInsumoCidade
from core.utils_calculo import atualizar_impacto_obra

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

class ImpactoObraTestCase(TestCase):
    def setUp(self):
        self.cuiaba = Cidade.objects.create(nome="Cuiabá", estado="MT")
        self.material = Material.objects.create(
            descricao="Concreto Teste",
            energia_embutida_mj_kg=10,
            co2_kg=0.2,
            fator_manutencao=1.1
        )
        self.insumo = Insumo.objects.create(
            codigo_sinapi="000001",
            descricao="Insumo Concreto",
            unidade="kg",
            material=self.material
        )
        DistanciaInsumoCidade.objects.create(insumo=self.insumo, cidade=self.cuiaba, km=50)

        self.composicao = Composicao.objects.create(
            codigo="COMP123",
            descricao="Composição Teste",
            unidade="m3"
        )
        ItemDeComposicao.objects.create(
            composicao_pai=self.composicao,
            insumo=self.insumo,
            unidade="kg",
            proporcao=100,
            valido=True
        )
        self.obra = Obra.objects.create(
            nome="Obra Teste",
            tipologia="Residencial",
            estado="MT",
            cidade=self.cuiaba,
            area_total_construir=100
        )
        EtapaConstrutiva.objects.create(
            obra=self.obra,
            nome="Fundação",
            dados={"composicoes": ["COMP123"]}
        )

    def test_atualizacao_impacto(self):
        resultado = atualizar_impacto_obra(self.obra)
        self.obra.refresh_from_db()
        itens = self.obra.itens_aplicados.all()
        self.assertEqual(itens.count(), 2)  # 1 composição + 1 insumo

        energia_total = self.obra.energia_embutida_total()
        co2_total = self.obra.co2_total()

        self.assertGreater(energia_total, 0)
        self.assertGreater(co2_total, 0)
        print("✅", resultado, f"Energia: {energia_total} MJ | CO2: {co2_total} kg")

