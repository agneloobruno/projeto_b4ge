    "use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function ImpactoResumo() {
  const router = useRouter();
  const [dados, setDados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState(null);

  const obraId = router.query?.id;

  useEffect(() => {
    if (!obraId) return;

    const token = localStorage.getItem("token");
    if (!token) {
      setErro("Token JWT não encontrado. Faça login novamente.");
      setLoading(false);
      return;
    }

    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/impactos/obra/${obraId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error("Erro ao buscar dados de impacto");
        return res.json();
      })
      .then((data) => {
        setDados(data);
        setLoading(false);
      })
      .catch((err) => {
        setErro(err.message);
        setLoading(false);
      });
  }, [obraId]);

  if (loading) return <p>Carregando...</p>;
  if (erro) return <p className="text-red-500">Erro: {erro}</p>;
  if (!dados || dados.length === 0) return <p>Nenhum dado encontrado.</p>;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">Impactos Ambientais por Etapa</h2>
      <table className="min-w-full border border-gray-200">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 text-left">Etapa</th>
            <th className="px-4 py-2 text-left">Energia Embutida (MJ)</th>
            <th className="px-4 py-2 text-left">CO₂ (kg)</th>
          </tr>
        </thead>
        <tbody>
          {dados.map((etapa, idx) => (
            <tr key={idx} className="border-t">
              <td className="px-4 py-2">{etapa.etapa_obra}</td>
              <td className="px-4 py-2">{etapa.energia_embutida_total}</td>
              <td className="px-4 py-2">{etapa.co2_total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
