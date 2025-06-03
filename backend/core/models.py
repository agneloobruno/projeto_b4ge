from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.postgres.fields import ArrayField

class Obras(models.Model):
    #cadastro de obra
    nome = models.CharField(max_length=100)
    razao_social = models.CharField(max_length=100, null=True, blank=True)

    tipologia = models.CharField(max_length=50)
    cep = models.CharField(max_length=10, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    municipio = models.CharField(max_length=50, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    area_terreno = models.FloatField(null=True, blank=True)
    area_total_construir = models.FloatField(null=True, blank=True)
    area_total_demolir = models.FloatField(null=True, blank=True)
    custo_inicial_estimado = models.FloatField(null=True, blank=True)
    custo_final_apurado = models.FloatField(null=True, blank=True)
    tipo_registro = models.CharField(max_length=50, null=True, blank=True)
    data_inicio_construcao = models.DateField(null=True, blank=True)
    data_termino_construcao = models.DateField(null=True, blank=True)
    sistema_construtivo = models.CharField(max_length=100, null=True, blank=True)

    tipo_empreendimento = models.CharField(max_length=50, null=True, blank=True)
    segmentacao = models.CharField(max_length=50, null=True, blank=True)
    padrao_empreendimento = models.CharField(max_length=50, null=True, blank=True)
    numero_unidades = models.IntegerField(null=True, blank=True)
    numero_pavimentos = models.IntegerField(null=True, blank=True)

    #Financiamento
    financiamento_publico = models.BooleanField(default=False)
    certificacao_obra = models.BooleanField(default=False)
    certificacao_obra_tipo = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.nome
    
    def energia_embutida_total(self):
        total = 0
        for insumo in self.insumos.all():
            total += insumo.quantidade_kg * insumo.material.energia_embutida_mj_kg * insumo.material.fator_manutencao
        return round(total, 2)

    def co2_total(self):
        total = 0
        for insumo in self.insumos.all():
            total += insumo.quantidade_kg * insumo.material.co2_kg * insumo.material.fator_manutencao
        return round(total, 2)

class Composicao(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    unidade = models.CharField(max_length=10)
    etapa_obra = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class ComposicaoItem(models.Model):
    composicao_pai = models.ForeignKey(Composicao, on_delete=models.CASCADE, related_name='itens')
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True, blank=True)
    subcomposicao = models.ForeignKey('Composicao', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_itens')
    unidade = models.CharField(max_length=10)
    proporcao = models.FloatField()

    def __str__(self):
        return f"{self.composicao_pai.codigo} → {self.material or self.subcomposicao}"


class Material(models.Model):
    descricao = models.CharField(max_length=255, unique=True)
    densidade = models.FloatField(null=True, blank=True)
    energia_embutida_mj_kg = models.FloatField(null=True, blank=True)
    energia_embutida_mj_m3 = models.FloatField(null=True, blank=True)
    co2_kg = models.FloatField(null=True, blank=True)
    fator_manutencao = models.FloatField(null=True, blank=True)
    referencia = models.CharField(max_length=255, null=True, blank=True)
    capacidade_caminhao = models.IntegerField(null=True, blank=True)
    referencia_para_cuiaba = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.descricao

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.nome} - {self.estado}"
    
class DistanciaTransporte(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    km = models.FloatField()

    def __str__(self):
        return f"{self.material.descricao} -> {self.cidade.nome}: {self.km} km"

class ItemLista(models.Model):
    obra = models.ForeignKey('Obras', on_delete=models.CASCADE, related_name="itens_lista")

    tipo = models.CharField(
        max_length=20,
        choices=[("INSUMO", "INSUMO"), ("COMPOSICAO", "COMPOSICAO")]
    )
    etapa_obra = models.CharField(max_length=100)

    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True, blank=True)
    composicao = models.ForeignKey('Composicao', on_delete=models.SET_NULL, null=True, blank=True)

    unidade = models.CharField(max_length=10, null=True, blank=True)
    proporcao = models.FloatField(null=True, blank=True)
    quantidade = models.FloatField(null=True, blank=True)
    equivalente_kg = models.FloatField(null=True, blank=True)

    energia_embutida_mj = models.FloatField(null=True, blank=True)
    energia_embutida_gj = models.FloatField(null=True, blank=True)
    co2_kg = models.FloatField(null=True, blank=True)

    distancia_km = models.FloatField(null=True, blank=True)
    energia_transporte_mj = models.FloatField(null=True, blank=True)
    energia_transporte_gj = models.FloatField(null=True, blank=True)

    potencia_w = models.FloatField(null=True, blank=True)
    tempo_uso = models.FloatField(null=True, blank=True)
    energia_equip_mj = models.FloatField(null=True, blank=True)
    energia_equip_gj = models.FloatField(null=True, blank=True)

    percentual_total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.obra.nome} - {self.tipo} - {self.material or self.composicao}"
