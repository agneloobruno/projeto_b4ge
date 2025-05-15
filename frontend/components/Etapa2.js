"use client";

import { useEffect, useState } from "react";

export default function Etapa2({ etapaAnterior, proximaEtapa, dados, setDados }) {
  const [materiais, setMateriais] = useState([]);
  const [insumosSelecionados, setInsumosSelecionados] = useState(dados.insumos || []);
  const [erro, setErro] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/materiais/")
      .then((res) => res.json())
      .then((data) => setMateriais(data));
  }, []);

  const adicionarInsumo = (materialId) => {
    const jaExiste = insumosSelecionados.find((i) => i.material === materialId);
    if (jaExiste) return;

    setInsumosSelecionados((prev) => [
      ...prev,
      { material: materialId, quantidade_kg: 0 },
    ]);
  };

  const atualizarQuantidade = (index, novaQtd) => {
    const atualizados = [...insumosSelecionados];
    atualizados[index].quantidade_kg = parseFloat(novaQtd);
    setInsumosSelecionados(atualizados);
  };

  const salvarEAvancar = () => {
    setErro(""); // limpa erro anterior

    if (insumosSelecionados.length === 0) {
      setErro("Você precisa selecionar pelo menos um material.");
      return;
    }

    const algumInvalido = insumosSelecionados.some(
      (insumo) =>
        !insumo.quantidade_kg ||
        isNaN(insumo.quantidade_kg) ||
        insumo.quantidade_kg <= 0
    );

    if (algumInvalido) {
      setErro("Informe quantidades válidas (maiores que 0) para todos os insumos.");
      return;
    }

    setDados({ ...dados, insumos: insumosSelecionados });
    proximaEtapa();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold mb-4">Selecione os materiais utilizados</h2>

      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {materiais.map((mat) => (
          <button
            key={mat.id}
            onClick={() => adicionarInsumo(mat.id)}
            className="bg-gray-800 px-4 py-2 rounded hover:bg-gray-700"
          >
            {mat.nome}
          </button>
        ))}
      </div>

      {insumosSelecionados.length > 0 && (
        <div className="mt-6">
          <h3 className="text-lg font-semibold mb-2">Materiais selecionados:</h3>
          <ul className="space-y-2">
            {insumosSelecionados.map((insumo, index) => {
              const mat = materiais.find((m) => m.id === insumo.material);
              return (
                <li key={index} className="flex items-center justify-between">
                  <span>{mat?.nome}</span>
                  <input
                    type="number"
                    value={insumo.quantidade_kg}
                    onChange={(e) => atualizarQuantidade(index, e.target.value)}
                    placeholder="Qtd (kg)"
                    className={`ml-4 p-1 rounded bg-gray-800 w-32 ${
                      erro &&
                      (!insumo.quantidade_kg || insumo.quantidade_kg <= 0)
                        ? "border border-red-500"
                        : "border border-gray-600"
                    }`}
                  />
                </li>
              );
            })}
          </ul>
        </div>
      )}

      <div className="flex justify-between mt-6">
        <button
          onClick={etapaAnterior}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500"
        >
          Voltar
        </button>
        <button
          onClick={salvarEAvancar}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Próxima etapa
        </button>
      </div>
    </div>
  );
}
