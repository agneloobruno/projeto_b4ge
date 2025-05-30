from django.db import models

class Obras(models.Model):
    nome = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=50)
    localizacao = models.CharField(max_length=100)
    area_construida = models.FloatField()

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
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, related_name="insumos")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_kg = models.FloatField()

    def __str__(self):
        return f"{self.material.descricao} em {self.obra.nome}"
