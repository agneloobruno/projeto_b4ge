export default function KPIs({
  energiaGJ, co2kg, gjm2, co2m2,
}: { energiaGJ: string; co2kg: string; gjm2: string; co2m2: string }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div className="card">
        <div className="text-sm opacity-70">Energia (GJ)</div>
        <div className="kpi">{Number(energiaGJ).toFixed(3)}</div>
      </div>
      <div className="card">
        <div className="text-sm opacity-70">CO₂e (kg)</div>
        <div className="kpi">{Number(co2kg).toFixed(1)}</div>
      </div>
      <div className="card">
        <div className="text-sm opacity-70">Intensidade (GJ/m²)</div>
        <div className="kpi">{Number(gjm2).toFixed(4)}</div>
      </div>
      <div className="card">
        <div className="text-sm opacity-70">Intensidade (kgCO₂e/m²)</div>
        <div className="kpi">{Number(co2m2).toFixed(3)}</div>
      </div>
    </div>
  );
}
