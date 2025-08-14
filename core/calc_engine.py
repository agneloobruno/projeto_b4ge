from decimal import Decimal, getcontext
from typing import Dict, List
from .models import (
    Obra, ItemDeComposicao, ConversaoMaterial, DistanciaInsumoCidade,
    FatorTransporte, ParametrosOperacionais, EtapaConstrutiva
)

getcontext().prec = 28

MJ_POR_GJ = Decimal('1000')
KCAL_POR_MJ = Decimal('239.005736')
MJ_POR_KCAL = Decimal('0.004184')

class LinhaResultado:
    def __init__(self, etapa: str):
        self.etapa = etapa
        self.energia_MJ = Decimal('0')
        self.co2e_kg = Decimal('0')
    def add(self, energia_MJ: Decimal, co2e_kg: Decimal):
        self.energia_MJ += energia_MJ
        self.co2e_kg += co2e_kg

def _aplicar_desperdicio(qtd: Decimal, pct: Decimal) -> Decimal:
    return qtd * (Decimal('1') + (pct or Decimal('0'))/Decimal('100'))

def _converter_para_kg(item: ItemDeComposicao) -> Decimal:
    qtd = Decimal(item.quantidade)
    qtd = _aplicar_desperdicio(qtd, Decimal(item.desperdicio_pct))
    if item.unidade_medida.lower() == 'kg':
        return qtd
    conv = ConversaoMaterial.objects.filter(
        material=item.material,
        origem_unidade=item.unidade_medida.lower(),
        destino_unidade='kg'
    ).order_by('-espessura_m').first()
    if not conv:
        return qtd
    return qtd * Decimal(conv.fator_massa_kg_por_origem)

def _energia_e_co2_material(item: ItemDeComposicao, massa_kg: Decimal) -> tuple[Decimal, Decimal]:
    m = item.material
    energia_MJ = Decimal('0')
    co2e_kg = Decimal('0')
    if m.energia_MJ_por_kg:
        energia_MJ += massa_kg * Decimal(m.energia_MJ_por_kg)
    elif m.energia_MJ_por_un and item.unidade_medida.lower() == m.unidade_base.lower():
        energia_MJ += Decimal(item.quantidade) * Decimal(m.energia_MJ_por_un)
    if m.co2e_kg_por_kg:
        co2e_kg += massa_kg * Decimal(m.co2e_kg_por_kg)
    elif m.co2e_kg_por_un and item.unidade_medida.lower() == m.unidade_base.lower():
        co2e_kg += Decimal(item.quantidade) * Decimal(m.co2e_kg_por_un)
    return energia_MJ, co2e_kg

def _transporte_para_item(obra: Obra, massa_kg: Decimal) -> tuple[Decimal, Decimal]:
    fator = FatorTransporte.objects.order_by('id').first()
    if not fator or massa_kg <= 0:
        return Decimal('0'), Decimal('0')
    # Fallback: sem distância por material, assume 0 km
    dist = DistanciaInsumoCidade.objects.filter(cidade=obra.cidade).first()
    km = Decimal(dist.distancia_km) if dist else Decimal('0')
    toneladas = massa_kg / Decimal('1000')
    energia_MJ = toneladas * km * Decimal(fator.energia_MJ_por_t_km)
    co2e_kg = toneladas * km * Decimal(fator.co2e_kg_por_t_km)
    return energia_MJ, co2e_kg

def _mao_de_obra(obra: Obra) -> tuple[Decimal, Decimal]:
    params = ParametrosOperacionais.objects.order_by('id').first()
    if not params:
        return Decimal('0'), Decimal('0')
    kcal = Decimal(params.fator_kcal_por_hora_pessoa) * Decimal(params.horas_por_dia) * Decimal(params.pessoas_por_equipe)
    energia_MJ = kcal * MJ_POR_KCAL
    co2e_kg = (energia_MJ / MJ_POR_GJ) * Decimal(params.fator_kgCO2e_por_GJ)
    return energia_MJ, co2e_kg

def calcular_impactos_obra(obra_id: int) -> Dict:
    obra = Obra.objects.select_related('cidade__estado').get(id=obra_id)
    etapas: Dict[str, LinhaResultado] = {k: LinhaResultado(k) for k, _ in EtapaConstrutiva.choices}
    itens = ItemDeComposicao.objects.select_related('composicao', 'material').filter(composicao__isnull=False)
    detalhamento: List[Dict] = []

    for item in itens:
        etapa = item.composicao.etapa
        massa_kg = _converter_para_kg(item)
        e_mat, c_mat = _energia_e_co2_material(item, massa_kg)
        e_transp, c_transp = _transporte_para_item(obra, massa_kg)
        etapas[etapa].add(e_mat + e_transp, c_mat + c_transp)
        detalhamento.append({
            'composicao': item.composicao.codigo,
            'etapa': etapa,
            'material': item.material.nome,
            'qtd': str(item.quantidade),
            'un': item.unidade_medida,
            'massa_kg': str(massa_kg),
            'energia_MJ_material': str(e_mat),
            'co2e_kg_material': str(c_mat),
            'energia_MJ_transporte': str(e_transp),
            'co2e_kg_transporte': str(c_transp),
        })

    e_mo, c_mo = _mao_de_obra(obra)
    etapas[EtapaConstrutiva.TRANSP_MO].add(e_mo, c_mo)

    total_MJ = sum((v.energia_MJ for v in etapas.values()), Decimal('0'))
    total_GJ = total_MJ / MJ_POR_GJ
    total_CO2e = sum((v.co2e_kg for v in etapas.values()), Decimal('0'))

    area = Decimal(obra.area_construida_m2) if obra.area_construida_m2 else Decimal('1')
    intensidade_GJ_m2 = (total_GJ / area) if area > 0 else Decimal('0')
    intensidade_kgCO2e_m2 = (total_CO2e / area) if area > 0 else Decimal('0')

    por_etapa = {
        k: {
            'energia_MJ': str(v.energia_MJ),
            'energia_GJ': str(v.energia_MJ / MJ_POR_GJ),
            'co2e_kg': str(v.co2e_kg)
        } for k, v in etapas.items()
    }

    return {
        'obra': {
            'id': int(obra.pk),
            'nome': obra.nome,
            'cidade': str(obra.cidade),
            'area_construida_m2': str(obra.area_construida_m2),
        },
        'totais': {
            'energia_MJ': str(total_MJ),
            'energia_GJ': str(total_GJ),
            'co2e_kg': str(total_CO2e),
        },
        'intensidades': {
            'GJ_m2': str(intensidade_GJ_m2),
            'kgCO2e_m2': str(intensidade_kgCO2e_m2),
        },
        'por_etapa': por_etapa,
        'detalhamento_itens': detalhamento,
    }
