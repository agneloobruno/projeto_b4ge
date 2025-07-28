'use client';

import { useState } from 'react';

const TIPOLOGIAS_VEDACAO = [
  'Alvenaria 14x9x19cm',
  'Oriented Strand Boards (OSB)',
  'Placa Cimentícia',
  'Tijolo ecológico estrutural',
  'Bloco de concreto estrutural (1:4:1) 14x19x39cm fck 4,5 mpa',
  'Light Steel Frame',
  'Taipa',
  'Adobe',
  'Madeira',
  'Alvenaria em Pedra'
];

export default function Etapa4_Vedacoes({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });

    if (erro) setErro('');
  };

  const validar = () => {
    if (
      !dados.tipologia_vedacao_externa ||
      !dados.area_paredes_externas ||
      !dados.tipologia_vedacao_interna ||
      !dados.area_paredes_internas
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
      <h2 className="text-2xl font-bold">Etapa 4 – Vedações</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Vedação Externa */}
        <fieldset className="border p-4 rounded-md">
          <legend className="text-sm font-semibold mb-2">Vedação Externa</legend>
          <div className="space-y-4">
            <label className="block">
              <span className="text-sm">Tipologia de vedação externa *</span>
              <select
                name="tipologia_vedacao_externa"
                value={dados.tipologia_vedacao_externa || ''}
                onChange={handleChange}
                className="input"
              >
                <option value="">Selecione</option>
                {TIPOLOGIAS_VEDACAO.map((tipo) => (
                  <option key={tipo} value={tipo}>{tipo}</option>
                ))}
              </select>
            </label>

            <input
              name="area_paredes_externas"
              value={dados.area_paredes_externas || ''}
              onChange={handleChange}
              className="input"
              placeholder="Área total das paredes externas (m²)"
            />
          </div>
        </fieldset>

        {/* Vedação Interna */}
        <fieldset className="border p-4 rounded-md">
          <legend className="text-sm font-semibold mb-2">Vedação Interna</legend>
          <div className="space-y-4">
            <label className="block">
              <span className="text-sm">Tipologia de vedação interna *</span>
              <select
                name="tipologia_vedacao_interna"
                value={dados.tipologia_vedacao_interna || ''}
                onChange={handleChange}
                className="input"
              >
                <option value="">Selecione</option>
                {TIPOLOGIAS_VEDACAO.map((tipo) => (
                  <option key={tipo} value={tipo}>{tipo}</option>
                ))}
              </select>
            </label>

            <input
              name="area_paredes_internas"
              value={dados.area_paredes_internas || ''}
              onChange={handleChange}
              className="input"
              placeholder="Área total das paredes internas (m²)"
            />
          </div>
        </fieldset>
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
