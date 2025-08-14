import KPIs from '@/components/KPIs';
import ImpactChart from '@/components/ImpactChart';
import { getImpactos } from '@/lib/api';

export default async function PageObra({ params }: { params: { id: string } }) {
  const data = await getImpactos(params.id);

  const etapas = Object.entries(data.por_etapa).map(([etapa, v]) => ({
    etapa,
    energia_GJ: Number(v.energia_GJ),
    co2e_kg: Number(v.co2e_kg),
  })).filter(x => x.energia_GJ > 0 || x.co2e_kg > 0);

  return (
    <main className="space-y-6">
      <div className="card">
        <div className="h2">{data.obra.nome}</div>
        <div className="text-sm opacity-70">{data.obra.cidade} • {data.obra.area_construida_m2} m²</div>
      </div>

      <KPIs
        energiaGJ={data.totais.energia_GJ}
        co2kg={data.totais.co2e_kg}
        gjm2={data.intensidades.GJ_m2}
        co2m2={data.intensidades.kgCO2e_m2}
      />

      <ImpactChart data={etapas} yKey="energia_GJ" yLabel="Energia (GJ)" />
      <ImpactChart data={etapas} yKey="co2e_kg" yLabel="CO₂e (kg)" />
    </main>
  );
}
