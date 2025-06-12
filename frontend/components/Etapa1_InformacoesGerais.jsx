'use client';

import { useState } from 'react';

export default function Etapa1_InformacoesGerais({ dados, setDados, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    const obrigatorios = ['tipologia', 'cep', 'estado', 'cidade', 'area_construida'];
    const faltando = obrigatorios.filter((campo) => !dados[campo]);
    if (faltando.length > 0) {
      setErro('Preencha todos os campos obrigatórios (*)');
      return false;
    }
    setErro('');
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 1 – Informações Gerais da Obra</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Tipologia da Edificação *</span>
          <select
            name="tipologia"
            value={dados.tipologia || ''}
            onChange={handleChange}
            className="input"
          >
            <option value="">Selecione uma tipologia</option>
            <option value="Escritório">Escritório</option>
            <option value="Educacional">Educacional</option>
            <option value="Hospedagem">Hospedagem</option>
            <option value="Assistência de saúde – EAS (exceto hospitais)">Assistência de saúde – EAS (exceto hospitais)</option>
            <option value="Varejo (comércio)">Varejo (comércio)</option>
            <option value="Varejo (mercado)">Varejo (mercado)</option>
            <option value="Alimentação (restaurantes)">Alimentação (restaurantes)</option>
            <option value="Edifícios não descritos anteriormente">Edifícios não descritos anteriormente</option>
          </select>
        </label>


        <input name="local_obra" onChange={handleChange} value={dados.local_obra || ''} className="input" placeholder="Local da Obra" />

        <input name="cep" onChange={handleChange} value={dados.cep || ''} className="input" placeholder="CEP *" />

        <input name="logradouro" onChange={handleChange} value={dados.logradouro || ''} className="input" placeholder="Logradouro" />
        <input name="numero" onChange={handleChange} value={dados.numero || ''} className="input" placeholder="Número" />
        <input name="bairro" onChange={handleChange} value={dados.bairro || ''} className="input" placeholder="Bairro" />

        <input name="estado" onChange={handleChange} value={dados.estado || ''} className="input" placeholder="Estado (UF) *" />
        <input name="cidade" onChange={handleChange} value={dados.cidade || ''} className="input" placeholder="Cidade *" />

        <input name="area_total" onChange={handleChange} value={dados.area_total || ''} className="input" placeholder="Área total (m²)" />
        <input name="area_construida" onChange={handleChange} value={dados.area_construida || ''} className="input" placeholder="Área construída (m²) *" />

        <input name="volume_demolir" onChange={handleChange} value={dados.volume_demolir || ''} className="input" placeholder="Volume a demolir (m³)" />
        <input name="escavacao_manual" onChange={handleChange} value={dados.escavacao_manual || ''} className="input" placeholder="Escavação horizontal em solo 1ª cat. (m³)" />
      </div>

      <button onClick={handleAvancar} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
        Próxima Etapa
      </button>
    </div>
  );
}
