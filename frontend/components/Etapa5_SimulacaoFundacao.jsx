'use client';

import { useState } from 'react';
import { authFetch } from '@/src/utils/authFetch';

const opcoesFundacao = [
  { codigo: '100001', nome: 'Fundação rasa em concreto ciclópico' },
  { codigo: '100002', nome: 'Fundação profunda com estacas' },
  { codigo: '100003', nome: 'Radier com tela dupla' },
  // Adicione conforme seus códigos do SINAPI
];

export default function Etapa5_SimulacaoFundacao({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [codigoSelecionado, setCodigoSelecionado] = useState('');
  const [resultado, setResultado] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState('');

  const simularFundacao = async () => {
    if (!codigoSelecionado) {
      setErro('Selecione um tipo de fundação para simular.');
      return;
    }

    setErro('');
    setCarregando(true);
    try {
      const res = await authFetch('http://localhost:8000/api/simular_fundacao/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ codigo: codigoSelecionado })
      });

      if (!res.ok) throw new Error('Erro ao simular fundação');

      const data = await res.json();
      setResultado(data);
    } catch (e) {
      setErro(e.message);
    } finally {
      setCarregando(false);
    }
  };

  const usarFundacaoNaObra = () => {
    setDados({
      ...dados,
      fundacao: {
        codigo: resultado.codigo,
        descricao: resultado.descricao,
        impacto: resultado.impacto
      }
    });
    proximaEtapa();
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 5 – Simulação de Fundação</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="space-y-2">
        {opcoesFundacao.map((f) => (
          <label key={f.codigo} className="flex items-center gap-2">
            <input
              type="radio"
              name="fundacao"
              value={f.codigo}
              checked={codigoSelecionado === f.codigo}
              onChange={(e) => setCodigoSelecionado(e.target.value)}
            />
            {f.nome}
          </label>
        ))}
      </div>

      <button
        onClick={simularFundacao}
        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
        disabled={carregando}
      >
        {carregando ? 'Simulando...' : 'Simular Fundação'}
      </button>

      {resultado && (
        <div className="bg-green-900 p-4 rounded space-y-2 mt-6">
          <p><strong>Código:</strong> {resultado.codigo}</p>
          <p><strong>Descrição:</strong> {resultado.descricao}</p>
          <p><strong>Energia Embutida:</strong> {resultado.impacto?.energia_mj} MJ</p>
          <p><strong>CO₂ Emitido:</strong> {resultado.impacto?.co2_kg} kg</p>

          <button
            onClick={usarFundacaoNaObra}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 mt-4"
          >
            Usar esta Fundação na Obra
          </button>
        </div>
      )}

      <div className="flex justify-between mt-6">
        <button
          onClick={etapaAnterior}
          className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-500"
        >
          Voltar
        </button>
      </div>
    </div>
  );
}
