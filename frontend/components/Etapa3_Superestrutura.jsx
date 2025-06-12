'use client';

import { useState } from 'react';

const TIPOS_SUPERESTRUTURA = [
  'Alvenaria com Cinta de Amarração',
  'Concreto Armado Moldado In Loco',
  'Estrutura Metálica',
  'Estrutura em Madeira',
  'Concreto Armado Pré-Moldado'
];

export default function Etapa3_Superestrutura({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    if (!dados.superestrutura_1 || !dados.superestrutura_2) {
      setErro('Selecione ambas as tipologias de superestrutura.');
      return false;
    }
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
    else setErro('Preencha os campos obrigatórios');
  };

  const renderCampos = (prefixo, tipo) => {
    switch (tipo) {
      case 'Alvenaria com Cinta de Amarração':
        return (
          <>
            <input name={`${prefixo}_cinta_comprimento`} value={dados[`${prefixo}_cinta_comprimento`] || ''} onChange={handleChange} className="input" placeholder="Comprimento da cinta (m)" />
            <input name={`${prefixo}_cinta_largura`} value={dados[`${prefixo}_cinta_largura`] || ''} onChange={handleChange} className="input" placeholder="Largura da cinta (cm)" />
          </>
        );
      case 'Concreto Armado Moldado In Loco':
        return (
          <>
            <input name={`${prefixo}_volume_vigas`} value={dados[`${prefixo}_volume_vigas`] || ''} onChange={handleChange} className="input" placeholder="Volume das vigas e pilares (m³)" />
            <input name={`${prefixo}_area_formas`} value={dados[`${prefixo}_area_formas`] || ''} onChange={handleChange} className="input" placeholder="Área das formas (m²)" />
            <input name={`${prefixo}_peso_armadura`} value={dados[`${prefixo}_peso_armadura`] || ''} onChange={handleChange} className="input" placeholder="Peso da armadura (kg)" />
          </>
        );
      case 'Estrutura Metálica':
        return (
          <input name={`${prefixo}_peso_armadura`} value={dados[`${prefixo}_peso_armadura`] || ''} onChange={handleChange} className="input" placeholder="Peso da armadura (kg)" />
        );
      case 'Estrutura em Madeira':
        return (
          <input name={`${prefixo}_comprimento_vigas`} value={dados[`${prefixo}_comprimento_vigas`] || ''} onChange={handleChange} className="input" placeholder="Comprimento das vigas e pilares (m)" />
        );
      case 'Concreto Armado Pré-Moldado':
        return (
          <input name={`${prefixo}_volume_estrutura`} value={dados[`${prefixo}_volume_estrutura`] || ''} onChange={handleChange} className="input" placeholder="Volume de concreto total (m³)" />
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 3 – Superestrutura</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Tipologia de Superestrutura 01 *</span>
          <select
            name="superestrutura_1"
            value={dados.superestrutura_1 || ''}
            onChange={handleChange}
            className="input"
          >
            <option value="">Selecione</option>
            {TIPOS_SUPERESTRUTURA.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>

        <label>
          <span className="text-sm">Tipologia de Superestrutura 02 *</span>
          <select
            name="superestrutura_2"
            value={dados.superestrutura_2 || ''}
            onChange={handleChange}
            className="input"
          >
            <option value="">Selecione</option>
            {TIPOS_SUPERESTRUTURA.map((tipo) => (
              <option key={tipo} value={tipo}>{tipo}</option>
            ))}
          </select>
        </label>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {dados.superestrutura_1 && renderCampos('s1', dados.superestrutura_1)}
        {dados.superestrutura_2 && renderCampos('s2', dados.superestrutura_2)}
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
