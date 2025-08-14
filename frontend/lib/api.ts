export type ObraPayload = {
  nome: string;
  cidade_id: number;
  area_construida_m2: string;
  fundacao_codigo?: string | null;
  supra_estrutura_1_codigo?: string | null;
  supra_estrutura_2_codigo?: string | null;
  fechamentos_codigo?: string | null;
  telhado_codigo?: string | null;
  piso_codigo?: string | null;
};

export type ImpactosResponse = {
  obra: { id: number; nome: string; cidade: string; area_construida_m2: string };
  totais: { energia_MJ: string; energia_GJ: string; co2e_kg: string };
  intensidades: { GJ_m2: string; kgCO2e_m2: string };
  por_etapa: Record<string, { energia_MJ: string; energia_GJ: string; co2e_kg: string }>;
  detalhamento_itens: Array<{
    composicao: string; etapa: string; material: string;
    qtd: string; un: string; massa_kg: string;
    energia_MJ_material: string; co2e_kg_material: string;
    energia_MJ_transporte: string; co2e_kg_transporte: string;
  }>;
};

const BASE = process.env.NEXT_PUBLIC_API_BASE ?? "http://127.0.0.1:8000/api";

export async function getCidades() {
  const r = await fetch(`${BASE}/cidades/`, { cache: 'no-store' });
  if (!r.ok) throw new Error('Falha ao listar cidades');
  return r.json();
}

export async function postObra(payload: ObraPayload) {
  const r = await fetch(`${BASE}/obras/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!r.ok) throw new Error('Falha ao criar obra');
  return r.json();
}

export async function getImpactos(id: string | number): Promise<ImpactosResponse> {
  const r = await fetch(`${BASE}/obras/${id}/impactos/`, { cache: 'no-store' });
  if (!r.ok) throw new Error('Falha ao obter impactos');
  return r.json();
}
