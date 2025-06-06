'use client';

import { useState } from 'react';

export default function Etapa1_InfoGeralEndereco({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validarCampos = () => {
    const camposObrigatorios = ['nome_obra', 'razao_social', 'cep', 'estado', 'municipio', 'logradouro'];
    for (let campo of camposObrigatorios) {
      if (!dados[campo] || dados[campo].trim() === '') {
        setErro('⚠️ Preencha todos os campos obrigatórios.');
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
      <h2 className="text-2xl font-bold">Etapa 1 – Informações Gerais e Endereço</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Nome da Obra *</span>
          <input
            type="text"
            name="nome_obra"
            value={dados.nome_obra || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Razão Social *</span>
          <input
            type="text"
            name="razao_social"
            value={dados.razao_social || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">CEP *</span>
          <input
            type="text"
            name="cep"
            value={dados.cep || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Estado *</span>
          <input
            type="text"
            name="estado"
            value={dados.estado || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Município *</span>
          <input
            type="text"
            name="municipio"
            value={dados.municipio || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label>
          <span className="text-sm">Logradouro *</span>
          <input
            type="text"
            name="logradouro"
            value={dados.logradouro || ''}
            onChange={handleChange}
            className="input"
          />
        </label>

        <label className="md:col-span-2">
          <span className="text-sm">Complemento</span>
          <input
            type="text"
            name="complemento"
            value={dados.complemento || ''}
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
