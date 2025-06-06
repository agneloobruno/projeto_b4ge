'use client';

import { useState } from 'react';

export default function Etapa3_Financiamento({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const valor = type === 'checkbox' ? checked : value;
    setDados({ ...dados, [name]: valor });
  };

  const validarCampos = () => {
    if (dados.financiamento_publico === undefined || dados.certificacao === undefined) {
      setErro('⚠️ Responda às perguntas obrigatórias.');
      return false;
    }
    setErro('');
    return true;
  };

  const handleAvancar = () => {
    if (validarCampos()) {
      proximaEtapa();
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 3 – Financiamento</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="space-y-4">
        <label className="block">
          <span className="text-sm font-medium">A obra tem financiamento público?</span>
          <div className="flex gap-4 mt-1">
            <label>
              <input
                type="radio"
                name="financiamento_publico"
                value="sim"
                checked={dados.financiamento_publico === 'sim'}
                onChange={handleChange}
              />
              <span className="ml-1">Sim</span>
            </label>
            <label>
              <input
                type="radio"
                name="financiamento_publico"
                value="nao"
                checked={dados.financiamento_publico === 'nao'}
                onChange={handleChange}
              />
              <span className="ml-1">Não</span>
            </label>
          </div>
        </label>

        <label className="block">
          <span className="text-sm font-medium">A obra já teve ou buscará alguma certificação?</span>
          <div className="flex gap-4 mt-1">
            <label>
              <input
                type="radio"
                name="certificacao"
                value="sim"
                checked={dados.certificacao === 'sim'}
                onChange={handleChange}
              />
              <span className="ml-1">Sim</span>
            </label>
            <label>
              <input
                type="radio"
                name="certificacao"
                value="nao"
                checked={dados.certificacao === 'nao'}
                onChange={handleChange}
              />
              <span className="ml-1">Não</span>
            </label>
          </div>
        </label>

        {dados.certificacao === 'sim' && (
          <label className="block">
            <span className="text-sm">Informe a certificação:</span>
            <input
              type="text"
              name="certificacao_nome"
              value={dados.certificacao_nome || ''}
              onChange={handleChange}
              className="input"
              placeholder="Ex: LEED, EDGE, AQUA..."
            />
          </label>
        )}
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
