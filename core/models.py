from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Estado(models.Model):
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=80)
    def __str__(self):
        return self.sigla

class Cidade(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')
    nome = models.CharField(max_length=120)
    codigo_ibge = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        unique_together = ('estado', 'nome')
    def __str__(self):
        return f"{self.nome}/{self.estado.sigla}"

class EtapaConstrutiva(models.TextChoices):
    FUNDACAO = 'fundacao', 'Fundação'
    ESTRUTURA = 'estrutura', 'Estrutura'
    FECHAMENTOS = 'fechamentos', 'Fechamentos'
    COBERTURA = 'cobertura', 'Cobertura/Laje'
    ACABAMENTOS = 'acabamentos', 'Acabamentos/Instalações'
    TRANSP_MO = 'transp_mo', 'Transporte/Mão de Obra'
    DEMOLICAO = 'demolicao', 'Demolição'

class Obra(models.Model):
    nome = models.CharField(max_length=160)
    cidade = models.ForeignKey(Cidade, on_delete=models.PROTECT, related_name='obras')
    area_construida_m2 = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator('0')])
    fundacao_codigo = models.CharField(max_length=50, blank=True, null=True)
    supra_estrutura_1_codigo = models.CharField(max_length=50, blank=True, null=True)
    supra_estrutura_2_codigo = models.CharField(max_length=50, blank=True, null=True)
    fechamentos_codigo = models.CharField(max_length=50, blank=True, null=True)
    telhado_codigo = models.CharField(max_length=50, blank=True, null=True)
    piso_codigo = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.nome

class Material(models.Model):
    nome = models.CharField(max_length=160, unique=True)
    unidade_base = models.CharField(max_length=20, default='kg', help_text='Unidade canônica: kg, m2, un, etc.')
    densidade_kg_m3 = models.DecimalField(max_digits=12, decimal_places=4, null=True, blank=True)
    energia_MJ_por_un = models.DecimalField(max_digits=14, decimal_places=6, null=True, blank=True)
    co2e_kg_por_un = models.DecimalField(max_digits=14, decimal_places=6, null=True, blank=True)
    energia_MJ_por_kg = models.DecimalField(max_digits=14, decimal_places=6, null=True, blank=True)
    co2e_kg_por_kg = models.DecimalField(max_digits=14, decimal_places=6, null=True, blank=True)
    def __str__(self):
        return self.nome

class ConversaoMaterial(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='conversoes')
    origem_unidade = models.CharField(max_length=20)   # ex: m2, un, m3
    destino_unidade = models.CharField(max_length=20, default='kg')
    espessura_m = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    fator_massa_kg_por_origem = models.DecimalField(max_digits=16, decimal_places=6)
    class Meta:
        unique_together = ('material', 'origem_unidade', 'destino_unidade', 'espessura_m')
    def __str__(self):
        return f"{self.material} {self.origem_unidade}->{self.destino_unidade}"

class Composicao(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nome = models.CharField(max_length=160)
    etapa = models.CharField(max_length=20, choices=EtapaConstrutiva.choices)
    def __str__(self):
        return f"[{self.codigo}] {self.nome}"

class ItemDeComposicao(models.Model):
    composicao = models.ForeignKey(Composicao, on_delete=models.CASCADE, related_name='itens')
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name='itens')
    unidade_medida = models.CharField(max_length=20, help_text='ex: m2, un, kg')
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator('0')])
    desperdicio_pct = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('0'), help_text='% 0-100')
    def __str__(self):
        return f"{self.composicao.codigo} - {self.material.nome}"

class DistanciaInsumoCidade(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='distancias')
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE, related_name='distancias_insumo')
    distancia_km = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator('0')])
    class Meta:
        unique_together = ('material', 'cidade')
    def __str__(self):
        return f"{self.material} @ {self.cidade}: {self.distancia_km} km"

class ParametrosOperacionais(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    fator_kcal_por_hora_pessoa = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('250.00'))
    pessoas_por_equipe = models.IntegerField(default=3)
    horas_por_dia = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('8.00'))
    fator_kgCO2e_por_GJ = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('74.1000'))
    fator_kgCO2e_eletricidade_por_GJ = models.DecimalField(max_digits=10, decimal_places=4, default=Decimal('63.1000'))
    def __str__(self):
        return self.nome

class FatorTransporte(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    energia_MJ_por_t_km = models.DecimalField(max_digits=12, decimal_places=6, default=Decimal('1.000000'))
    co2e_kg_por_t_km = models.DecimalField(max_digits=12, decimal_places=6, default=Decimal('0.070000'))
    def __str__(self):
        return self.nome

class Desperdicio(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    etapa = models.CharField(max_length=20, choices=EtapaConstrutiva.choices, null=True, blank=True)
    percentual = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal('0'))
    def __str__(self):
        return f"{self.nome} ({self.percentual}%)"