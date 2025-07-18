"use client";

import { useEffect, useState } from "react";

export default function ImpactoResumo({ obraId }) {
  const [dados, setDados]     = useState([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro]       = useState(null);

  useEffect(() => {
    console.log("🔍 ImpactoResumo.useEffect iniciado para obraId =", obraId);

    if (!obraId) {
      console.log("⛔ Sem obraId — saindo do useEffect");
      setLoading(false);
      return;
    }

    // aqui pegamos o mesmo nome de chave que o LoginForm salva:
    const token = localStorage.getItem("accessToken");
    console.log("🔑 Token obtido:", token);

    if (!token) {
      console.log("⚠️ Token ausente — abortando fetch");
      setErro("Token JWT não encontrado. Faça login novamente.");
      setLoading(false);
      return;
    }

    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/impactos/obra/${obraId}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    )
      .then((res) => {
        console.log("🎯 ImpactoResumo → resposta status", res.status);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((data) => {
        console.log("🎉 ImpactoResumo → dados recebidos", data);
        setDados(data);
      })
      .catch((err) => {
        console.error("⚠️ ImpactoResumo → erro no fetch", err);
        setErro(err.message);
      })
      .finally(() => {
        console.log("✅ ImpactoResumo → carregamento finalizado");
        setLoading(false);
      });
  }, [obraId]);

  if (loading)       return <p>Carregando...</p>;
  if (erro)          return <p className="text-red-500">Erro: {erro}</p>;
  if (!dados.length) return <p>Nenhum dado encontrado.</p>;

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
