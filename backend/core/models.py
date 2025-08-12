from django.db import models, transaction
from django.db.models import Sum

# ---------------------------
# Catálogos e fatores
# ---------------------------

class Material(models.Model):
    descricao = models.CharField(max_length=255, unique=True)
    densidade_kg_m3 = models.FloatField(null=True, blank=True)

    # Fatores da planilha "Banco Materiais"
    energia_mj_kg = models.FloatField(null=True, blank=True)           # (col B) energia por kg
    fator_comp_L = models.FloatField(null=True, blank=True)            # (col C) multiplicador L
    fator_emissao_material_E = models.FloatField(null=True, blank=True)# (col E)
    fator_emissao_total_F = models.FloatField(null=True, blank=True)   # (col F)
    coef_transporte_O = models.FloatField(null=True, blank=True)       # (col H)
    divisor_para_massa_P = models.FloatField(null=True, blank=True)    # (col I) usado p/ Q = K/P

    fonte = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["descricao"]

    def __str__(self):
        return self.descricao


class Insumo(models.Model):
    codigo_sinapi = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    unidade = models.CharField(max_length=10, null=True, blank=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_sinapi} - {self.descricao}"


class Estado(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    sigla = models.CharField(max_length=2, unique=True)
    nome = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="cidades")

    def __str__(self):
        return f"{self.nome} - {self.estado.sigla}"


class DistanciaInsumoCidade(models.Model):
    insumo = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    cidade = models.ForeignKey(Cidade, on_delete=models.CASCADE)
    km = models.FloatField()

    class Meta:
        unique_together = ("insumo", "cidade")

    def __str__(self):
        return f"{self.insumo.codigo_sinapi} -> {self.cidade}: {self.km} km"


class Desperdicio(models.Model):
    """Percentual padrão de desperdício por material e/ou etapa (0..1)."""
    material = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    etapa_obra = models.CharField(max_length=100, null=True, blank=True)
    percentual = models.FloatField(default=0.0)  # guarde como 0..1

    class Meta:
        unique_together = ("material", "etapa_obra")


class ParametroGlobal(models.Model):
    """Parâmetros globais (ex.: EMISSAO_KGCO2_POR_GJ=74.1)."""
    chave = models.CharField(max_length=100, unique=True)
    valor = models.FloatField()
    obs = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.chave}={self.valor}"


class FatorTransporte(models.Model):
    """Fatores como E10, E11 da planilha 'Transp - MO'."""
    nome = models.CharField(max_length=50, unique=True)  # ex.: E10, E11
    mj_por_kg_km = models.FloatField()
    obs = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.nome}={self.mj_por_kg_km}"


# ---------------------------
# Obra e etapas (dados brutos)
# ---------------------------

ETAPAS = [
    ("FUNDACAO", "Fundação"),
    ("ESTRUTURA", "Estrutura"),
    ("VEDACOES", "Vedações"),
    ("COBERTURA", "Cobertura"),
    ("CONTRAPISO", "Contrapiso"),
    ("ESQUADRIAS", "Esquadrias"),
    ("REVESTIMENTOS", "Revestimentos"),
    ("INSTALACOES", "Instalações"),
    ("MAO_DE_OBRA", "Mão de Obra"),
    ("DEMOLICAO", "Demolição"),
]

class Obra(models.Model):
    nome = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=50, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    estado = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    area_construida = models.FloatField(null=True, blank=True)
    area_total = models.FloatField(null=True, blank=True)
    area_terreno = models.FloatField(null=True, blank=True)
    area_total_construir = models.FloatField(null=True, blank=True)
    area_total_demolir = models.FloatField(null=True, blank=True)

    # Totais calculados
    energia_total_mj = models.FloatField(null=True, blank=True)
    co2_total_kg = models.FloatField(null=True, blank=True)

    def calcular_impacto_total(self):
        impacto = self.itens_aplicados.aggregate(
            total_energia_mj=Sum("energia_total_mj"),
            total_co2_kg=Sum("co2_total_kg"),
        )
        self.energia_total_mj = impacto["total_energia_mj"] or 0.0
        self.co2_total_kg = impacto["total_co2_kg"] or 0.0
        self.save(update_fields=["energia_total_mj", "co2_total_kg"])


class EtapaConstrutiva(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="etapas_tecnicas")
    nome = models.CharField(max_length=100, choices=ETAPAS)
    dados = models.JSONField()  # guarda TUDO que o wizard manda por etapa
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.obra.nome} - {self.nome}"


# --------------------------------
# Composições (se você usa)
# --------------------------------

class Composicao(models.Model):
    TIPO_CHOICES = [("SERVICO","Serviço"), ("COMPOSICAO","Composição"), ("INSUMO","Insumo")]
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, default="COMPOSICAO")
    codigo = models.CharField(max_length=50, unique=True)
    descricao = models.TextField()
    unidade = models.CharField(max_length=10)
    etapa_obra = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"


class ItemDeComposicao(models.Model):
    composicao_pai = models.ForeignKey(Composicao, on_delete=models.CASCADE, related_name="itens")
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT, null=True, blank=True, related_name="composicao_items")
    subcomposicao = models.ForeignKey(Composicao, on_delete=models.SET_NULL, null=True, blank=True, related_name="como_subcomposicao")
    unidade = models.CharField(max_length=10)
    proporcao = models.FloatField(null=True, blank=True)
    valido = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.composicao_pai.codigo} → {self.insumo or self.subcomposicao}"


# -------------------------
# Insumos aplicados na obra
# -------------------------

class InsumoAplicado(models.Model):
    obra = models.ForeignKey(Obra, related_name="itens_aplicados", on_delete=models.CASCADE)
    etapa_obra = models.CharField(max_length=100, choices=ETAPAS)

    # referência
    insumo = models.ForeignKey(Insumo, on_delete=models.PROTECT)
    # entradas brutas
    quantidade = models.FloatField(null=True, blank=True)
    unidade = models.CharField(max_length=20, null=True, blank=True)  # kg, t, m3, l, un
    distancia_km = models.FloatField(null=True, blank=True)
    potencia_w = models.FloatField(null=True, blank=True)
    tempo_uso_h = models.FloatField(null=True, blank=True)
    percentual_desperdicio = models.FloatField(null=True, blank=True)  # 0..1

    # derivados (sempre calculados no back)
    q_kg = models.FloatField(null=True, blank=True, editable=False)  # massa equivalente
    energia_material_mj = models.FloatField(null=True, blank=True, editable=False)   # M
    energia_transporte_mj = models.FloatField(null=True, blank=True, editable=False) # R
    energia_equip_mj = models.FloatField(null=True, blank=True, editable=False)      # V
    energia_desperdicio_mj = models.FloatField(null=True, blank=True, editable=False)# Y
    energia_transp_descarte_mj = models.FloatField(null=True, blank=True, editable=False) # AA
    energia_total_mj = models.FloatField(null=True, blank=True, editable=False)      # AB
    energia_total_gj = models.FloatField(null=True, blank=True, editable=False)      # AC

    co2_por_gj_kg = models.FloatField(null=True, blank=True, editable=False)         # AJ (por energia total)
    co2_material_kg = models.FloatField(null=True, blank=True, editable=False)       # AI
    co2_total_fator_kg = models.FloatField(null=True, blank=True, editable=False)    # AG
    co2_total_kg = models.FloatField(null=True, blank=True, editable=False)          # soma dos canais

    calculado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        from .services.calculo import calcular_item, atualizar_totais_obra

        # completa defaults (ex.: distância por cidade/insumo)
        if self.distancia_km is None and self.obra_id and self.insumo_id and self.obra.cidade_id:
            try:
                self.distancia_km = float(
                    DistanciaInsumoCidade.objects.filter(
                        insumo_id=self.insumo_id, cidade_id=self.obra.cidade_id
                    ).values_list("km", flat=True).first() or 0.0
                )
            except Exception:
                self.distancia_km = 0.0

        # aplica cálculo
        deriv = calcular_item(self)
        for k, v in deriv.items():
            setattr(self, k, v)

        super().save(*args, **kwargs)

        if self.obra_id:
            transaction.on_commit(lambda: atualizar_totais_obra(self.obra))
