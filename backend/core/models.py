from django.db import models

class Obras(models.Model):
    nome = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=100)
    localizacao = models.CharField(max_length=100)
    area_construida = models.FloatField(help_text="Área construída em m²")

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
            total += insumo.quantidade_kg * insumo.material.co2eq_kg * insumo.material.fator_manutencao
        return round(total, 2)
    
class Material(models.Model):
    nome = models.CharField(max_length=100)
    densidade_kg_m3 = models.FloatField()
    energia_embutida_mj_kg = models.FloatField()
    co2eq_kg = models.FloatField()
    fator_manutencao = models.FloatField(default=1.0)
    distancia_transporte_km = models.FloatField()
    referencia = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.nome
    
class InsumoUsado(models.Model):
    obra = models.ForeignKey(Obras, on_delete=models.CASCADE, related_name="insumos")
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantidade_kg = models.FloatField()

    def __str__(self):
        return f"{self.material.nome} em {self.obra.nome}"
