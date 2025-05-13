"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Etapa3({ dados, etapaAnterior }) {
  const router = useRouter(); 
  const [resultado, setResultado] = useState(null);
  const [enviando, setEnviando] = useState(false);

  const enviarSimulacao = async () => {
    try {
      setEnviando(true);
      const resposta = await fetch("http://localhost:8000/api/simular/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });

      if (!resposta.ok) throw new Error("Erro ao enviar dados para simulação");

      const resultadoBackend = await resposta.json();
      setResultado(resultadoBackend);
    } catch (err) {
      alert("Erro: " + err.message);
    } finally {
      setEnviando(false);
    }
  };

  const salvarObra = async () => {
  try {
      const resposta = await fetch("http://localhost:8000/api/salvar/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });

      if (!resposta.ok) throw new Error("Erro ao salvar obra");

     alert("✅ Obra salva com sucesso!");
     router.push("/obras");
    } catch (err) {
     alert("❌ " + err.message);
    }
  };


  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Resumo da Obra</h2>

      <div className="bg-gray-800 p-4 rounded space-y-1">
        <p><strong>Nome:</strong> {dados.nome}</p>
        <p><strong>Tipologia:</strong> {dados.tipologia}</p>
        <p><strong>Localização:</strong> {dados.localizacao}</p>
        <p><strong>Área construída:</strong> {dados.area_construida} m²</p>
      </div>

      <div className="bg-gray-800 p-4 rounded">
        <h3 className="text-lg font-semibold mb-2">Materiais utilizados</h3>
        {dados.insumos.length === 0 ? (
          <p className="text-sm text-gray-400">Nenhum insumo selecionado.</p>
        ) : (
          <ul className="space-y-1">
            {dados.insumos.map((ins, idx) => (
              <li key={idx}>
                {`Material ${ins.material}`}: {ins.quantidade_kg} kg
              </li>
            ))}
          </ul>
        )}
      </div>

      {resultado && (
        <><div className="bg-green-800 p-4 rounded space-y-1">
          <p><strong>Energia Total:</strong> {resultado.energia_total} MJ</p>
          <p><strong>CO₂ Total:</strong> {resultado.co2_total} kg</p>
        </div><button onClick={salvarObra} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Salvar Obra no Sistema</button></>
      )}

      <div className="flex justify-between mt-6">
        <button
          onClick={etapaAnterior}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500"
        >
          Voltar
        </button>
        <button
          onClick={enviarSimulacao}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
          disabled={enviando}
        >
          {enviando ? "Calculando..." : "Finalizar"}
        </button>
      </div>
    </div>
  );
}
