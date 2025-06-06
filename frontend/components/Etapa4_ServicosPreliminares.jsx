'use client';

import { useState } from 'react';

export default function Etapa4_ServicosPreliminares({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [movSolo, setMovSolo] = useState(dados.movimentacao_solo || []);
  const [combustiveis, setCombustiveis] = useState(dados.combustiveis || []);
  const [observacoes, setObservacoes] = useState(dados.observacoes || []);
  const [erro, setErro] = useState('');

  const handleAddMovimentacao = () => {
    setMovSolo([...movSolo, {
      solo_transportado: '',
      distancia_total: '',
      unidade: '',
      percurso_estimado: '',
      fonte: '',
      data_entrega_material: ''
    }]);
  };

  const handleAddCombustivel = () => {
    setCombustiveis([...combustiveis, {
      descricao_maquina: '',
      tipo_combustivel: '',
      quantidade_horas: '',
      unidade: '',
      fonte: '',
      data_entrega_combustivel: ''
    }]);
  };

  const handleAddObservacao = () => {
    setObservacoes([...observacoes, { texto: '' }]);
  };

  const handleInputChange = (setter, index, field, value) => {
    setter((prev) => {
      const atualizados = [...prev];
      atualizados[index][field] = value;
      return atualizados;
    });
  };

  const handleSalvar = () => {
    setDados({
      ...dados,
      movimentacao_solo: movSolo,
      combustiveis: combustiveis,
      observacoes: observacoes
    });
    proximaEtapa();
  };

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold">Etapa 4 – Serviços Preliminares</h2>

      {/* 4.1 - Movimentação de Solo */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">4.1 – Movimentação de Solo</h3>
        {movSolo.map((item, idx) => (
          <div key={idx} className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-gray-800 p-3 rounded">
            <input className="input" placeholder="Solo transportado" value={item.solo_transportado}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'solo_transportado', e.target.value)} />
            <input className="input" placeholder="Distância total (km)" value={item.distancia_total}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'distancia_total', e.target.value)} />
            <input className="input" placeholder="Unidade" value={item.unidade}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'unidade', e.target.value)} />
            <input className="input" placeholder="Percursos estimados" value={item.percurso_estimado}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'percurso_estimado', e.target.value)} />
            <input className="input" placeholder="Fonte (própria/terceira)" value={item.fonte}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'fonte', e.target.value)} />
            <input className="input" type="date" value={item.data_entrega_material}
              onChange={(e) => handleInputChange(setMovSolo, idx, 'data_entrega_material', e.target.value)} />
          </div>
        ))}
        <button onClick={handleAddMovimentacao} className="btn">Adicionar Movimentação</button>
      </div>

      {/* 4.2 - Combustíveis */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">4.2 – Uso de Combustíveis em Máquinas</h3>
        {combustiveis.map((item, idx) => (
          <div key={idx} className="grid grid-cols-1 md:grid-cols-3 gap-3 bg-gray-800 p-3 rounded">
            <input className="input" placeholder="Descrição da máquina" value={item.descricao_maquina}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'descricao_maquina', e.target.value)} />
            <input className="input" placeholder="Tipo de combustível" value={item.tipo_combustivel}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'tipo_combustivel', e.target.value)} />
            <input className="input" placeholder="Qtd. horas utilizadas" value={item.quantidade_horas}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'quantidade_horas', e.target.value)} />
            <input className="input" placeholder="Unidade" value={item.unidade}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'unidade', e.target.value)} />
            <input className="input" placeholder="Fonte" value={item.fonte}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'fonte', e.target.value)} />
            <input className="input" type="date" value={item.data_entrega_combustivel}
              onChange={(e) => handleInputChange(setCombustiveis, idx, 'data_entrega_combustivel', e.target.value)} />
          </div>
        ))}
        <button onClick={handleAddCombustivel} className="btn">Adicionar Combustível</button>
      </div>

      {/* 4.3 - Observações */}
      <div className="space-y-4">
        <h3 className="text-lg font-semibold">4.3 – Observações</h3>
        {observacoes.map((item, idx) => (
          <textarea
            key={idx}
            className="input w-full"
            placeholder="Escreva sua observação..."
            value={item.texto}
            onChange={(e) => handleInputChange(setObservacoes, idx, 'texto', e.target.value)}
          />
        ))}
        <button onClick={handleAddObservacao} className="btn">Adicionar Observação</button>
      </div>

      {/* Navegação */}
      <div className="flex justify-between mt-6">
        <button onClick={etapaAnterior} className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500">
          Voltar
        </button>
        <button onClick={handleSalvar} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
          Próxima Etapa
        </button>
      </div>
    </div>
  );
}
