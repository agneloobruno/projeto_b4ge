# models.py atualizado com melhorias para cálculo de impacto e estrutura relacional

from django.db import models

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
    
    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materiais"
        ordering = ['descricao']


class Insumo(models.Model):
    codigo_sinapi = models.CharField(max_length=20, unique=True)
    descricao = models.TextField()
    unidade = models.CharField(max_length=10)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True)


    def __str__(self):
        return f"{self.codigo_sinapi} - {self.descricao}"

class Estado(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    regiao = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name='cidades')

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class DistanciaInsumoCidade(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    km = models.FloatField()

    def __str__(self):
        return f"{self.insumo.descricao} -> {self.cidade.nome}: {self.km} km"


class Obra(models.Model):
    # Informações básicas da obra
    nome = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=50)
    cep = models.CharField(max_length=10, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    area_terreno = models.FloatField(null=True, blank=True)
    area_total_construir = models.FloatField(null=True, blank=True)
    area_total_demolir = models.FloatField(null=True, blank=True)

    #tipologias fundação
    tipologia_fundacao = models.CharField(max_length=50, null=True, blank=True)
    radier_espessura = models.IntegerField(null=True, blank=True)
    radier_area_total = models.FloatField(null=True, blank=True)

    #tipologias superestrutura
    superestrutura_1 = models.CharField(max_length=50, null=True, blank=True)
    superestrutura_2 = models.CharField(max_length=50, null=True, blank=True)
    tipologia_vedacao_externa = models.CharField(max_length=50, null=True, blank=True)
    tipologia_vedacao_interna = models.CharField(max_length=50, null=True, blank=True)


    def __str__(self):
        return self.nome

    def energia_embutida_total(self):
        total = 0
        for item in self.itens_aplicados.all():
            total += (item.energia_embutida_mj or 0) + (item.energia_transporte_mj or 0) + (item.energia_equip_mj or 0)
        return round(total, 2)

    def co2_total(self):
        return round(sum((item.co2_kg or 0) for item in self.itens_aplicados.all()), 2)
    
    energia_total_mj = models.FloatField(null=True, blank=True)
    co2_total_kg = models.FloatField(null=True, blank=True)



class Composicao(models.Model):
    TIPO_CHOICES = [
        ("SERVICO", "Serviço"),
        ("COMPOSICAO", "Composição"),
        ("INSUMO", "Insumo"),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default="COMPOSICAO")
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    unidade = models.CharField(max_length=10)
    etapa_obra = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao} ({self.get_tipo_display()})"



class ItemDeComposicao(models.Model):
    composicao_pai = models.ForeignKey(Composicao, on_delete=models.CASCADE, related_name='itens')
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, null=True, blank=True, related_name="composicao_items")
    subcomposicao = models.ForeignKey(Composicao, on_delete=models.SET_NULL, null=True, blank=True, related_name="como_subcomposicao")
    unidade = models.CharField(max_length=10)
    proporcao = models.FloatField(null=True, blank=True)
    valido = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.composicao_pai.codigo} → {self.insumo or self.subcomposicao}"


class InsumoAplicado(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="itens_aplicados")
    tipo = models.CharField(max_length=20, choices=[("INSUMO", "INSUMO"), ("COMPOSICAO", "COMPOSICAO")])
    etapa_obra = models.CharField(max_length=100)

    insumo = models.ForeignKey(Insumo, on_delete=models.SET_NULL, null=True, blank=True)
    composicao = models.ForeignKey(Composicao, on_delete=models.SET_NULL, null=True, blank=True)

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
        return f"{self.obra.nome} - {self.tipo} - {self.insumo or self.composicao}"


class EtapaConstrutiva(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='etapas_tecnicas')
    nome = models.CharField(max_length=100)
    dados = models.JSONField()
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.obra.nome} - {self.nome}"
    

class ImpactoInsumoComposicao(models.Model):
    composicao_pai = models.ForeignKey(Composicao, on_delete=models.CASCADE)
    insumo = models.ForeignKey('Insumo', on_delete=models.CASCADE)
    unidade = models.CharField(max_length=10)
    proporcao = models.FloatField()

    quantidade = models.FloatField(null=True, blank=True)
    energia_embutida_total = models.FloatField(null=True, blank=True)
    carbono_embutido = models.FloatField(null=True, blank=True)
    carbono_transporte = models.FloatField(null=True, blank=True)
    carbono_manutencao = models.FloatField(null=True, blank=True)
    carbono_despesa = models.FloatField(null=True, blank=True)
    carbono_total = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.insumo} na {self.composicao_pai}"

