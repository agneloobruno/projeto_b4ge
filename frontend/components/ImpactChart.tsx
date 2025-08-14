'use client';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

export default function ImpactChart({
  data, yKey, yLabel
}: { data: Array<{ etapa: string; energia_GJ: number; co2e_kg: number }>; yKey: 'energia_GJ' | 'co2e_kg'; yLabel: string; }) {
  return (
    <div className="card">
      <div className="h2 mb-2">{yLabel} por etapa</div>
      <div style={{ width: '100%', height: 320 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="etapa" />
            <YAxis />
            <Tooltip />
            <Bar dataKey={yKey} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
