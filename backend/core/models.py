from django.db import models

class Obra(models.Model):
    nome = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cep = models.CharField(max_length=10)
    estado = models.CharField(max_length=2)
    municipio = models.CharField(max_length=100)
    logradouro = models.CharField(max_length=255)
    complemento = models.CharField(max_length=255, blank=True, null=True)

    area_terreno = models.FloatField()
    area_construir = models.FloatField()
    area_demolir = models.FloatField()
    custo_inicial_estimado = models.FloatField()
    custo_final_apurado = models.FloatField(null=True, blank=True)
    tipo_registro = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_termino = models.DateField(null=True, blank=True)
    sistema_construtivo = models.CharField(max_length=100)
    especificacao = models.CharField(max_length=255)
    tipo_empreendimento = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=100)
    segmentacao = models.CharField(max_length=100)
    padrao_empreendimento = models.CharField(max_length=100)
    numero_unidades = models.IntegerField()
    numero_pavimentos = models.IntegerField()

    financiamento_publico = models.BooleanField(default=False)
    busca_certificacao = models.BooleanField(default=False)
    certificacao_informada = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class MovimentacaoSolo(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='movimentacoes_solo')
    solo_transportado_m3 = models.FloatField()
    solo_recebido_m3 = models.FloatField()
    solo_destinado_m3 = models.FloatField()
    distancia_total_km = models.FloatField()
    unidade_medida = models.CharField(max_length=20)
    estimativa_percursos = models.IntegerField()
    fonte = models.CharField(max_length=100)
    data_entrega_material = models.DateField()
    evidencia = models.TextField(blank=True, null=True)

class UsoCombustivelMaquina(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='usos_combustiveis')
    descricao_maquina = models.CharField(max_length=255)
    tipo_combustivel = models.CharField(max_length=100)
    combustivel_utilizado_litros = models.FloatField()
    qtd_horas_utilizadas = models.FloatField()
    unidade = models.CharField(max_length=20)
    fonte = models.CharField(max_length=100)
    data_entrega_combustivel = models.DateField()
    evidencia = models.TextField(blank=True, null=True)

class ObservacaoObra(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='observacoes')
    observacao = models.TextField()

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

class InsumoUsado(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="insumos")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_kg = models.FloatField()

    def __str__(self):
        return f"{self.material.descricao} em {self.obra.nome}"
