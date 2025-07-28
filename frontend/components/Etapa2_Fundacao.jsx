'use client';

import { useState } from 'react';

const TIPOS_FUNDACAO = ['Radier', 'Sapata', 'Tubulão', 'Estaca', 'Viga baldrame'];

const valoresEspessuraRadier = [10, 15, 20, 25, 30];
const valoresDiametroTubulao = [70, 80, 100, 120];
const valoresDiametroEstaca = [30, 50, 70, 90];

export default function Etapa2_Fundacao({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    if (!dados.tipologia_fundacao) {
      setErro('Selecione uma tipologia de fundação.');
      return false;
    }
    setErro('');
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
  };

  const tipo = dados.tipologia_fundacao;

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 2 – Fundação</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <label className="block">
        <span className="text-sm">Tipologia de Fundação *</span>
        <select
          name="tipologia_fundacao"
          value={dados.tipologia_fundacao || ''}
          onChange={handleChange}
          className="input"
        >
          <option value="">Selecione</option>
          {TIPOS_FUNDACAO.map((tipo) => (
            <option key={tipo} value={tipo}>{tipo}</option>
          ))}
        </select>
      </label>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {tipo === 'Radier' && (
          <>
            <input
              name="radier_area_total"
              onChange={handleChange}
              value={dados.radier_area_total || ''}
              className="input"
              placeholder="Área total (m²)"
            />
            <div>
              <label className="block text-sm mb-2">Espessura (cm)</label>
              <div className="grid grid-cols-3 gap-2">
                {valoresEspessuraRadier.map((esp) => (
                  <label key={esp} className="flex items-center gap-1">
                    <input
                      type="radio"
                      name="radier_espessura"
                      value={esp}
                      checked={dados.radier_espessura === esp.toString()}
                      onChange={handleChange}
                    />
                    {esp}
                  </label>
                ))}
              </div>
            </div>
          </>
        )}

        {tipo === 'Sapata' && (
          <>
            <input name="sapata_area_forma" onChange={handleChange} value={dados.sapata_area_forma || ''} className="input" placeholder="Área total de forma das sapatas (m²)" />
            <input name="sapata_volume_concreto" onChange={handleChange} value={dados.sapata_volume_concreto || ''} className="input" placeholder="Volume total de concreto (m³)" />
            <input name="sapata_peso_armadura" onChange={handleChange} value={dados.sapata_peso_armadura || ''} className="input" placeholder="Peso da armação (kg) Aço CA" />
          </>
        )}

        {tipo === 'Tubulão' && (
          <>
            <input name="tubulao_volume_total" onChange={handleChange} value={dados.tubulao_volume_total || ''} className="input" placeholder="Volume total (m³)" />
            <div>
              <label className="block text-sm mb-2">Diâmetro (cm)</label>
              <div className="grid grid-cols-3 gap-2">
                {valoresDiametroTubulao.map((diam) => (
                  <label key={diam} className="flex items-center gap-1">
                    <input
                      type="radio"
                      name="tubulao_diametro"
                      value={diam}
                      checked={dados.tubulao_diametro === diam.toString()}
                      onChange={handleChange}
                    />
                    {diam}
                  </label>
                ))}
              </div>
            </div>
            <input name="tubulao_profundidade" onChange={handleChange} value={dados.tubulao_profundidade || ''} className="input" placeholder="Profundidade (m)" />
          </>
        )}

        {tipo === 'Estaca' && (
          <>
            <input name="estaca_volume_total" onChange={handleChange} value={dados.estaca_volume_total || ''} className="input" placeholder="Volume total (m³)" />
            <div>
              <label className="block text-sm mb-2">Diâmetro (cm)</label>
              <div className="grid grid-cols-3 gap-2">
                {valoresDiametroEstaca.map((diam) => (
                  <label key={diam} className="flex items-center gap-1">
                    <input
                      type="radio"
                      name="estaca_diametro"
                      value={diam}
                      checked={dados.estaca_diametro === diam.toString()}
                      onChange={handleChange}
                    />
                    {diam}
                  </label>
                ))}
              </div>
            </div>
            <input name="estaca_profundidade" onChange={handleChange} value={dados.estaca_profundidade || ''} className="input" placeholder="Profundidade (m)" />
          </>
        )}

        {tipo === 'Viga baldrame' && (
          <>
            <input name="viga_forma" onChange={handleChange} value={dados.viga_forma || ''} className="input" placeholder="Área de forma (m²)" />
            <input name="viga_volume" onChange={handleChange} value={dados.viga_volume || ''} className="input" placeholder="Volume (m³)" />
            <input name="viga_aco" onChange={handleChange} value={dados.viga_aco || ''} className="input" placeholder="Aço CA-50 (kg)" />
          </>
        )}
      </div>

      <div className="flex justify-between mt-6">
        <button onClick={etapaAnterior} className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500">
          Voltar
        </button>
        <button onClick={handleAvancar} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Próxima Etapa
        </button>
      </div>
    </div>
  );
}
