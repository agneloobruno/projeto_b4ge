"use client";

import { useState } from "react";

export default function Etapa1({ dados, onChange, proximaEtapa }) {
  const [erro, setErro] = useState("");

  const handleAvancar = () => {
    setErro(""); // limpa erros anteriores

    if (
      !dados.nome.trim() ||
      !dados.tipologia.trim() ||
      !dados.localizacao.trim() ||
      !dados.area_construida ||
      isNaN(dados.area_construida) ||
      Number(dados.area_construida) <= 0
    ) {
      setErro("⚠️ Preencha todos os campos corretamente antes de continuar.");
      return;
    }

    proximaEtapa();
  };

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Dados da Obra</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <label className="block">
        <span className="text-sm">Nome da Obra</span>
        <input
          type="text"
          name="nome"
          value={dados.nome}
          onChange={onChange}
          className={`w-full p-2 rounded bg-gray-800 ${
            erro && !dados.nome.trim()
              ? "border border-red-500"
              : "border border-gray-700"
          }`}
          required
        />
      </label>

      <label className="block">
        <span className="text-sm">Tipologia</span>
        <input
          type="text"
          name="tipologia"
          value={dados.tipologia}
          onChange={onChange}
          className={`w-full p-2 rounded bg-gray-800 ${
            erro && !dados.tipologia.trim()
              ? "border border-red-500"
              : "border border-gray-700"
          }`}
          required
        />
      </label>

      <label className="block">
        <span className="text-sm">Localização</span>
        <input
          type="text"
          name="localizacao"
          value={dados.localizacao}
          onChange={onChange}
          className={`w-full p-2 rounded bg-gray-800 ${
            erro && !dados.localizacao.trim()
              ? "border border-red-500"
              : "border border-gray-700"
          }`}
          required
        />
      </label>

      <label className="block">
        <span className="text-sm">Área construída (m²)</span>
        <input
          type="number"
          name="area_construida"
          value={dados.area_construida}
          onChange={onChange}
          className={`w-full p-2 rounded bg-gray-800 ${
            erro &&
            (!dados.area_construida ||
              isNaN(dados.area_construida) ||
              Number(dados.area_construida) <= 0)
              ? "border border-red-500"
              : "border border-gray-700"
          }`}
          required
        />
      </label>

      <button
        onClick={handleAvancar}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Próxima etapa
      </button>
    </div>
  );
}
