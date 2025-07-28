'use client';

import { useState } from 'react';

const TIPOLOGIAS_LAJE = [
  { id: 1, label: 'Pré-moldada' },
  { id: 2, label: 'Alveolar' }
];

const TIPOLOGIAS_TELHADO = [
  { id: 1, label: 'Telha fibrocimento' },
  { id: 2, label: 'Telha cerâmica' },
  { id: 3, label: 'Telha metálica' },
  { id: 4, label: 'Telha termoacústica' },
  { id: 5, label: 'Outro' }
];

const TIPOLOGIAS_ESTRUTURA = ['Estrutura em madeira', 'Estrutura metálica', 'Outro'];
const TIPOLOGIAS_FORRO = ['Madeira', 'Drywall', 'Placas de gesso', 'Outro'];

export default function Etapa5_Cobertura({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const valor = type === 'checkbox' ? checked : value;
    setDados({ ...dados, [name]: valor });

    if (erro) setErro('');
  };

  const validar = () => {
    if (dados.laje_forro === 'S') {
      if (!dados.area_laje || !dados.volume_laje || !dados.peso_armadura_laje || !dados.tipologia_laje) {
        setErro('Preencha os dados obrigatórios da laje.');
        return false;
      }
    }
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
    else setErro('Verifique os campos obrigatórios.');
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 5 – Cobertura</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Configurações principais */}
        <fieldset className="border p-4 rounded-md space-y-4">
          <legend className="text-sm font-semibold">Configurações</legend>

          <label className="block">
            <span className="text-sm">Laje de Cobertura para forro *</span>
            <select name="laje_forro" value={dados.laje_forro || ''} onChange={handleChange} className="input">
              <option value="">Selecione</option>
              <option value="S">S</option>
              <option value="N">N</option>
            </select>
          </label>

          <label className="block">
            <span className="text-sm">Possui Platibanda *</span>
            <select name="platibanda" value={dados.platibanda || ''} onChange={handleChange} className="input">
              <option value="">Selecione</option>
              <option value="S">S</option>
              <option value="N">N</option>
            </select>
          </label>

          <label className="block">
            <span className="text-sm">Tipologia de Telhamento</span>
            <select name="tipologia_telhado" value={dados.tipologia_telhado || ''} onChange={handleChange} className="input">
              <option value="">Selecione</option>
              {TIPOLOGIAS_TELHADO.map((tipo) => (
                <option key={tipo.id} value={tipo.id}>
                  {tipo.id} - {tipo.label}
                </option>
              ))}
            </select>
          </label>

          <label className="block">
            <span className="text-sm">Tipologia de Estrutura</span>
            <select name="tipologia_estrutura" value={dados.tipologia_estrutura || ''} onChange={handleChange} className="input">
              <option value="">Selecione</option>
              {TIPOLOGIAS_ESTRUTURA.map((tipo) => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </label>

          <label className="block">
            <span className="text-sm">Tipologia de Forro</span>
            <select name="tipologia_forro" value={dados.tipologia_forro || ''} onChange={handleChange} className="input">
              <option value="">Selecione</option>
              {TIPOLOGIAS_FORRO.map((tipo) => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </label>
        </fieldset>

        {/* Dimensões gerais */}
        <fieldset className="border p-4 rounded-md space-y-4">
          <legend className="text-sm font-semibold">Dimensões Gerais</legend>

          <input
            name="area_coberta"
            value={dados.area_coberta || ''}
            onChange={handleChange}
            className="input"
            placeholder="Área coberta (m²)"
          />
          <input
            name="area_telhado"
            value={dados.area_telhado || ''}
            onChange={handleChange}
            className="input"
            placeholder="Área telhado (m²)"
          />
          <input
            name="comp_caibros"
            value={dados.comp_caibros || ''}
            onChange={handleChange}
            className="input"
            placeholder="Comprimento total caibros (m)"
          />
          <input
            name="comp_cumeeira"
            value={dados.comp_cumeeira || ''}
            onChange={handleChange}
            className="input"
            placeholder="Comprimento cumeeira (m)"
          />
          <input
            name="area_forro"
            value={dados.area_forro || ''}
            onChange={handleChange}
            className="input"
            placeholder="Área forro (m²)"
          />
          <input
            name="comprimento_calha"
            value={dados.comprimento_calha || ''}
            onChange={handleChange}
            className="input"
            placeholder="Calha (m)"
          />
          <input
            name="comprimento_rufo"
            value={dados.comprimento_rufo || ''}
            onChange={handleChange}
            className="input"
            placeholder="Rufo (m)"
          />
        </fieldset>

        {/* Detalhes da laje condicional */}
        {dados.laje_forro === 'S' && (
          <fieldset className="md:col-span-2 border p-4 rounded-md space-y-4">
            <legend className="text-sm font-semibold">Detalhes da Laje</legend>

            <input
              name="area_laje"
              value={dados.area_laje || ''}
              onChange={handleChange}
              className="input"
              placeholder="Área da forma da Laje (m²)"
            />
            <input
              name="volume_laje"
              value={dados.volume_laje || ''}
              onChange={handleChange}
              className="input"
              placeholder="Volume da Laje (m³)"
            />
            <input
              name="peso_armadura_laje"
              value={dados.peso_armadura_laje || ''}
              onChange={handleChange}
              className="input"
              placeholder="Peso da armação da laje (kg)"
            />

            <label className="block">
              <span className="text-sm">Tipologia de Laje *</span>
              <select name="tipologia_laje" value={dados.tipologia_laje || ''} onChange={handleChange} className="input">
                <option value="">Selecione</option>
                {TIPOLOGIAS_LAJE.map((tipo) => (
                  <option key={tipo.id} value={tipo.id}>
                    {tipo.id} - {tipo.label}
                  </option>
                ))}
              </select>
            </label>
          </fieldset>
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
