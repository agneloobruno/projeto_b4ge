'use client';

import { useState } from 'react';

const TIPOLOGIAS_LAJE = ['Pré-moldada', 'Alveolar'];
const TIPOLOGIAS_TELHADO = ['Telha fibrocimento', 'Telha cerâmica', 'Telha metálica', 'Outro'];
const TIPOLOGIAS_ESTRUTURA = ['Estrutura em madeira', 'Estrutura metálica', 'Outro'];
const TIPOLOGIAS_FORRO = ['Madeira', 'Drywall', 'Placas de gesso', 'Outro'];

export default function Etapa5_Cobertura({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    const valor = type === 'checkbox' ? checked : value;
    setDados({ ...dados, [name]: valor });
  };

  const validar = () => {
    if (!dados.area_laje || !dados.volume_laje || !dados.peso_armadura_laje) {
      setErro('Preencha os dados obrigatórios da laje.');
      return false;
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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Possui laje de forro? *</span>
          <select name="laje_forro" value={dados.laje_forro || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            <option value="S">Sim</option>
            <option value="N">Não</option>
          </select>
        </label>

        <label>
          <span className="text-sm">Possui platibanda? *</span>
          <select name="platibanda" value={dados.platibanda || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            <option value="S">Sim</option>
            <option value="N">Não</option>
          </select>
        </label>

        <label>
          <span className="text-sm">Tipologia da laje *</span>
          <select name="tipologia_laje" value={dados.tipologia_laje || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            {TIPOLOGIAS_LAJE.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>

        <input name="area_laje" value={dados.area_laje || ''} onChange={handleChange} className="input" placeholder="Área da laje (m²)" />
        <input name="volume_laje" value={dados.volume_laje || ''} onChange={handleChange} className="input" placeholder="Volume da laje (m³)" />
        <input name="peso_armadura_laje" value={dados.peso_armadura_laje || ''} onChange={handleChange} className="input" placeholder="Peso da armadura (kg)" />

        <label>
          <span className="text-sm">Tipologia de Telhamento</span>
          <select name="tipologia_telhado" value={dados.tipologia_telhado || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            {TIPOLOGIAS_TELHADO.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>

        <label>
          <span className="text-sm">Tipologia da Estrutura</span>
          <select name="tipologia_estrutura" value={dados.tipologia_estrutura || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            {TIPOLOGIAS_ESTRUTURA.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>

        <label>
          <span className="text-sm">Tipologia de Forro</span>
          <select name="tipologia_forro" value={dados.tipologia_forro || ''} onChange={handleChange} className="input">
            <option value="">Selecione</option>
            {TIPOLOGIAS_FORRO.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>

        <input name="area_coberta" value={dados.area_coberta || ''} onChange={handleChange} className="input" placeholder="Área coberta (m²)" />
        <input name="area_telhado" value={dados.area_telhado || ''} onChange={handleChange} className="input" placeholder="Área do telhado (m²)" />
        <input name="comp_caibros" value={dados.comp_caibros || ''} onChange={handleChange} className="input" placeholder="Comprimento total dos caibros (m)" />
        <input name="comp_cumeeira" value={dados.comp_cumeeira || ''} onChange={handleChange} className="input" placeholder="Comprimento da cumeeira (m)" />
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
