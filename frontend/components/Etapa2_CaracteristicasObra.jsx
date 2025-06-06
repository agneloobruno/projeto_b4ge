'use client';

import { useState } from 'react';

export default function Etapa2_CaracteristicasObra({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validarCampos = () => {
    const obrigatorios = ['area_terreno', 'area_construir_prefeitura', 'custo_estimado', 'tipo_registro'];
    for (let campo of obrigatorios) {
      if (!dados[campo] || dados[campo].toString().trim() === '') {
        setErro('⚠️ Preencha os campos obrigatórios.');
        return false;
      }
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
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Etapa 2 – Características da Obra</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Área do Terreno (m²)</span>
          <input
            type="number"
            name="area_terreno"
            value={dados.area_terreno || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Área a Construir - Prefeitura (m²)</span>
          <input
            type="number"
            name="area_construir_prefeitura"
            value={dados.area_construir_prefeitura || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Área a Demolir (m²)</span>
          <input
            type="number"
            name="area_demolir"
            value={dados.area_demolir || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Custo Estimado (R$)</span>
          <input
            type="number"
            name="custo_estimado"
            value={dados.custo_estimado || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Custo Final Apurado (R$)</span>
          <input
            type="number"
            name="custo_final"
            value={dados.custo_final || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Tipo de Registro</span>
          <input
            type="text"
            name="tipo_registro"
            value={dados.tipo_registro || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Data de Início da Construção</span>
          <input
            type="date"
            name="data_inicio"
            value={dados.data_inicio || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Data de Término da Construção</span>
          <input
            type="date"
            name="data_termino"
            value={dados.data_termino || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label className="md:col-span-2">
          <span className="text-sm">Sistema Construtivo</span>
          <input
            type="text"
            name="sistema_construtivo"
            value={dados.sistema_construtivo || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label className="md:col-span-2">
          <span className="text-sm">Tipo de Empreendimento</span>
          <input
            type="text"
            name="tipo_empreendimento"
            value={dados.tipo_empreendimento || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Tipologia</span>
          <input
            type="text"
            name="tipologia"
            value={dados.tipologia || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Segmentação do Empreendimento</span>
          <input
            type="text"
            name="segmentacao"
            value={dados.segmentacao || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Padrão do Empreendimento</span>
          <input
            type="text"
            name="padrao"
            value={dados.padrao || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Número de Unidades</span>
          <input
            type="number"
            name="numero_unidades"
            value={dados.numero_unidades || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Número de Pavimentos</span>
          <input
            type="number"
            name="numero_pavimentos"
            value={dados.numero_pavimentos || ''}
            onChange={handleChange}
            className="input"
          />
        </label>
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
