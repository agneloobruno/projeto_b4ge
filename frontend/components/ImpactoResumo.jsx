// frontend/components/ImpactoResumo.jsx
"use client";

import { useEffect, useState } from "react";

export default function ImpactoResumo({ obraId }) {
  const [dados, setDados]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro]       = useState(null);

  useEffect(() => {
    if (!obraId) {
      setLoading(false);
      return;
    }

    // pegar sempre do mesmo key
    const token = localStorage.getItem("accessToken");
    console.log("🔑 accessToken em ImpactoResumo:", token);

    if (!token) {
      setErro("Token JWT não encontrado. Faça login novamente.");
      setLoading(false);
      return;
    }

    const endpoint = `http://localhost:8000/api/impactos/obra/${obraId}/`;
    console.log("📡 ImpactoResumo chamando:", endpoint);

    fetch(endpoint, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => {
        console.log("🎯 resposta status", res.status);
        if (res.status === 401) {
          // token expirou ou é inválido
          localStorage.clear();
          window.location.href = "/login";
          return [];
        }
        if (res.status === 404) {
          return [];
        }
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((data) => setDados(data))
      .catch((err) => setErro(err.message))
      .finally(() => setLoading(false));
  }, [obraId]);

  if (loading)       return <p>Carregando...</p>;
  if (erro)          return <p className="text-red-500">Erro: {erro}</p>;
  if (!dados.length) return <p>Nenhum dado encontrado.</p>;

  return (
    <div className="mt-6">
      <h2 className="text-xl font-bold mb-4">
        Impactos Ambientais por Etapa
      </h2>
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
              <td className="px-4 py-2">
                {etapa.energia_embutida_total}
              </td>
              <td className="px-4 py-2">{etapa.co2_total}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
