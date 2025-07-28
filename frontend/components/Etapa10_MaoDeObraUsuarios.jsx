'use client';

import { useState } from 'react';

export default function Etapa10_MaoDeObraUsuarios({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Substitui vírgula por ponto para garantir compatibilidade numérica
    setDados({ ...dados, [name]: value.replace(',', '.') });
  };

  const parseNumber = (valor) => {
    return valor ? String(valor).replace('.', ',') : '';
  };

  const validar = () => {
    if (
      !dados.lotacao_transporte ||
      !dados.distancia_media ||
      !dados.consumo_diesel ||
      !dados.gasto_calorico ||
      !dados.estimativa_usuarios
    ) {
      setErro('Preencha todos os campos obrigatórios.');
      return false;
    }
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 10 – Mão de Obra e Usuários</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="border rounded p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Informações de transporte e uso</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label>
            <span className="text-sm">Lotação do transporte (pessoas)</span>
            <input
              type="text"
              name="lotacao_transporte"
              value={parseNumber(dados.lotacao_transporte)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Distância média (km)</span>
            <input
              type="text"
              name="distancia_media"
              value={parseNumber(dados.distancia_media)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Consumo de diesel (km/L)</span>
            <input
              type="text"
              name="consumo_diesel"
              value={parseNumber(dados.consumo_diesel)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Gasto calórico diário (kcal)</span>
            <input
              type="text"
              name="gasto_calorico"
              value={parseNumber(dados.gasto_calorico)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Estimativa de usuários da edificação</span>
            <input
              type="text"
              name="estimativa_usuarios"
              value={parseNumber(dados.estimativa_usuarios)}
              onChange={handleChange}
              className="input"
            />
          </label>
        </div>
      </div>

      <div className="flex justify-between mt-6">
        <button
          onClick={etapaAnterior}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500"
        >
          Voltar
        </button>
        <button
          onClick={handleAvancar}
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Finalizar
        </button>
      </div>
    </div>
  );
}
