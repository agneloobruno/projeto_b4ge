'use client';

import { useState } from 'react';

export default function Etapa10_MaoDeObraUsuarios({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    if (!dados.lotacao_transporte || !dados.distancia_media || !dados.consumo_diesel || !dados.gasto_calorico || !dados.estimativa_usuarios) {
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="number"
          name="lotacao_transporte"
          value={dados.lotacao_transporte || ''}
          onChange={handleChange}
          className="input"
          placeholder="Lotação do transporte (pessoas)"
        />

        <input
          type="number"
          name="distancia_media"
          value={dados.distancia_media || ''}
          onChange={handleChange}
          className="input"
          placeholder="Distância média (km)"
        />

        <input
          type="number"
          name="consumo_diesel"
          value={dados.consumo_diesel || ''}
          onChange={handleChange}
          className="input"
          placeholder="Consumo de diesel (km/L)"
        />

        <input
          type="number"
          name="gasto_calorico"
          value={dados.gasto_calorico || ''}
          onChange={handleChange}
          className="input"
          placeholder="Gasto calórico diário (kcal)"
        />

        <input
          type="number"
          name="estimativa_usuarios"
          value={dados.estimativa_usuarios || ''}
          onChange={handleChange}
          className="input"
          placeholder="Estimativa de usuários da edificação"
        />
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
