'use client';

import { useState } from 'react';

export default function Etapa10_MaoDeObraUsuarios({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const valores_padrao = {
    nome: "teste",
    tipologia: "teste",
    cep: "teste",
    estado: "MT",
    cidade: "Cuiabá",
    area_construida: "100",
    tipologia_fundacao: "Radier",
    superestrutura_1: "Concreto Armado Moldado In Loco",
    superestrutura_2: "Estrutura Metálica",
    tipologia_vedacao_externa: "Alvenaria 14x9x19cm",
    area_paredes_externas: "10",
    tipologia_vedacao_interna: "Alvenaria 14x9x19cm",
    area_paredes_internas: "10",
    area_laje: "10",
    volume_laje: "10",
    peso_armadura_laje: "1000",
    possui_contrapiso: "Não",
    tipologia_piso: "Cerâmico",
    area_revestimento: "10",
    comprimento_eletrodutos: "10",
    comprimento_fios: "10",
    lotacao_transporte: "10",
    distancia_media: "10",
    consumo_diesel: "10",
    gasto_calorico: "10",
    estimativa_usuarios: "2"
  }

  const validar = () => {
    if (!dados.lotacao_transporte || !dados.distancia_media || !dados.consumo_diesel || !dados.gasto_calorico || !dados.estimativa_usuarios) {
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
      <h2 className="text-2xl font-bold">Etapa 10 – Mão de Obra e Usuários</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <input
          type="number"
          name="lotacao_transporte"
          value={dados.lotacao_transporte || ''}
          onChange={handleChange}
          className="input"
          placeholder="Lotação do transporte (pessoas)"
        />

        <input
          type="number"
          name="distancia_media"
          value={dados.distancia_media || ''}
          onChange={handleChange}
          className="input"
          placeholder="Distância média (km)"
        />

        <input
          type="number"
          name="consumo_diesel"
          value={dados.consumo_diesel || ''}
          onChange={handleChange}
          className="input"
          placeholder="Consumo de diesel (km/L)"
        />

        <input
          type="number"
          name="gasto_calorico"
          value={dados.gasto_calorico || ''}
          onChange={handleChange}
          className="input"
          placeholder="Gasto calórico diário (kcal)"
        />

        <input
          type="number"
          name="estimativa_usuarios"
          value={dados.estimativa_usuarios || ''}
          onChange={handleChange}
          className="input"
          placeholder="Estimativa de usuários da edificação"
        />
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
          className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
        >
          Finalizar
        </button>
      </div>
    </div>
  );
}
