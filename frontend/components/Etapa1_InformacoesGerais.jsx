// frontend/components/Etapa1_InformacoesGerais.jsx
'use client';

import { useState, useEffect } from 'react';

export default function Etapa1_InformacoesGerais({ dados, setDados, proximaEtapa }) {
  const [erro, setErro] = useState('');
  const [estados, setEstados] = useState([]);
  const [cidadesFiltradas, setCidadesFiltradas] = useState([]);

  // 1) Carrega lista de estados
  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/estados/`)
      .then(res => res.json())
      .then(data => setEstados(data))
      .catch(err => console.error('Erro ao carregar estados:', err));
  }, []);

  // 2) Sempre que mudar o estado, carrega as cidades correspondentes
  useEffect(() => {
    if (!dados.estado) {
      setCidadesFiltradas([]);
      return;
    }
    fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/estados/${dados.estado}/cidades/`
    )
      .then(res => res.json())
      .then(data => setCidadesFiltradas(data))
      .catch(err => console.error('Erro ao carregar cidades:', err));
  }, [dados.estado]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    // Atualiza o campo correspondente em dados
    setDados(prev => ({ ...prev, [name]: value }));
  };

  const validar = () => {
    const obrigatorios = [
      'nome',
      'tipologia',
      'cep',
      'estado',
      'cidade',
      'area_construida'
    ];
    const faltando = obrigatorios.filter(c => !dados[c]);
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
      <h2 className="text-2xl font-bold">
        Etapa 1 – Informações Gerais da Obra
      </h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      {/* Dados Básicos */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          name="nome"
          onChange={handleChange}
          value={dados.nome || ''}
          className="input"
          placeholder="Nome da Obra *"
        />

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
            <option value="Assistência de saúde – EAS (exceto hospitais)">Assistência de saúde – EAS</option>
            <option value="Varejo (comércio)">Varejo (comércio)</option>
            <option value="Varejo (mercado)">Varejo (mercado)</option>
            <option value="Alimentação (restaurantes)">Restaurante</option>
            <option value="Outros">Outros</option>
          </select>
        </label>
      </div>

      {/* Localização */}
      <fieldset className="border border-gray-700 rounded-md p-4">
        <legend className="text-sm font-semibold px-2">
          📍 Localização da Obra
        </legend>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <input
            name="cep"
            onChange={handleChange}
            value={dados.cep || ''}
            className="input"
            placeholder="CEP *"
          />
          <input
            name="logradouro"
            onChange={handleChange}
            value={dados.logradouro || ''}
            className="input"
            placeholder="Logradouro"
          />
          <input
            name="numero"
            onChange={handleChange}
            value={dados.numero || ''}
            className="input"
            placeholder="Número"
          />
          <input
            name="bairro"
            onChange={handleChange}
            value={dados.bairro || ''}
            className="input"
            placeholder="Bairro"
          />

          <label>
            <span className="text-sm">Estado (UF) *</span>
            <select
              name="estado"
              value={dados.estado || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione o estado</option>
              {estados.map(e => (
                <option key={e.uf} value={e.uf}>
                  {e.nome} ({e.uf})
                </option>
              ))}
            </select>
          </label>

          <label>
            <span className="text-sm">Cidade *</span>
            <select
              name="cidade"
              value={dados.cidade || ''}
              onChange={handleChange}
              className="input"
              disabled={!dados.estado}
            >
              <option value="">Selecione a cidade</option>
              {cidadesFiltradas.map(c => (
                <option key={c.id} value={c.id}>
                  {c.nome}
                </option>
              ))}
            </select>
          </label>
        </div>
      </fieldset>

      {/* Área e Dimensões */}
      <fieldset className="border border-gray-700 rounded-md p-4">
        <legend className="text-sm font-semibold px-2">
          📐 Área e Dimensões
        </legend>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-2">
          <input
            name="area_total"
            onChange={handleChange}
            value={dados.area_total || ''}
            className="input"
            placeholder="Área total (m²)"
          />
          <input
            name="area_construida"
            onChange={handleChange}
            value={dados.area_construida || ''}
            className="input"
            placeholder="Área construída (m²) *"
          />
          <input
            name="volume_demolir"
            onChange={handleChange}
            value={dados.volume_demolir || ''}
            className="input"
            placeholder="Volume a demolir (m³)"
          />
          <input
            name="escavacao_manual"
            onChange={handleChange}
            value={dados.escavacao_manual || ''}
            className="input"
            placeholder="Escavação manual (m³)"
          />
        </div>
      </fieldset>

      <button
        onClick={handleAvancar}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 mt-4"
      >
        Próxima Etapa
      </button>
    </div>
  );
}
