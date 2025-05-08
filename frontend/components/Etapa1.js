"use client";

export default function Etapa1({ dados, onChange, proximaEtapa }) {
  return (
    <div className="space-y-4">
      <label className="block">
        <span className="text-sm">Nome da Obra</span>
        <input
          type="text"
          name="nome"
          value={dados.nome}
          onChange={onChange}
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
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
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
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
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
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
          className="w-full p-2 rounded bg-gray-800 border border-gray-700"
          required
        />
      </label>

      <button
        onClick={proximaEtapa}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      >
        Próxima etapa
      </button>
    </div>
  );
}
