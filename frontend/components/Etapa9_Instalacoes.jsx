'use client';

import { useState } from 'react';

export default function Etapa9_Instalacoes({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    if (!dados.comprimento_eletrodutos || !dados.comprimento_fios) {
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
      <h2 className="text-2xl font-bold">Etapa 9 – Instalações</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="number"
          name="comprimento_eletrodutos"
          value={dados.comprimento_eletrodutos || ''}
          onChange={handleChange}
          className="input"
          placeholder="Comprimento total dos eletrodutos (m)"
        />

        <input
          type="number"
          name="comprimento_fios"
          value={dados.comprimento_fios || ''}
          onChange={handleChange}
          className="input"
          placeholder="Comprimento total dos fios (m)"
        />

        <input
          type="number"
          name="bitolas_eletrodutos"
          value={dados.bitolas_eletrodutos || ''}
          onChange={handleChange}
          className="input"
          placeholder="Bitola dos eletrodutos (mm)"
        />

        <input
          type="number"
          name="bitolas_fios"
          value={dados.bitolas_fios || ''}
          onChange={handleChange}
          className="input"
          placeholder="Bitola dos fios (mm²)"
        />

        <input
          type="number"
          name="comprimento_tubos_pvc"
          value={dados.comprimento_tubos_pvc || ''}
          onChange={handleChange}
          className="input"
          placeholder="Comprimento total de tubos PVC (m)"
        />

        <input
          type="number"
          name="comprimento_tubos_cobre"
          value={dados.comprimento_tubos_cobre || ''}
          onChange={handleChange}
          className="input"
          placeholder="Comprimento total de tubos de cobre (m)"
        />

        <input
          type="number"
          name="divisorias_granito"
          value={dados.divisorias_granito || ''}
          onChange={handleChange}
          className="input"
          placeholder="Número de divisórias de granito"
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
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Próxima Etapa
        </button>
      </div>
    </div>
  );
}
