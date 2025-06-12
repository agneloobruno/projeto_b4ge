'use client';

import { useState } from 'react';

export default function Etapa7_Esquadrias({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    // Nenhum campo obrigatório, mas você pode incluir se desejar
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
    else setErro('Verifique os campos preenchidos.');
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 7 – Esquadrias</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

        {/* Portas */}
        <input name="portas_60x210" value={dados.portas_60x210 || ''} onChange={handleChange} className="input" placeholder="Qtd portas 60x210" />
        <input name="portas_70x210" value={dados.portas_70x210 || ''} onChange={handleChange} className="input" placeholder="Qtd portas 70x210" />
        <input name="portas_80x210" value={dados.portas_80x210 || ''} onChange={handleChange} className="input" placeholder="Qtd portas 80x210" />
        <input name="portas_120x210" value={dados.portas_120x210 || ''} onChange={handleChange} className="input" placeholder="Qtd portas 120x210" />
        <input name="portas_aluminio" value={dados.portas_aluminio || ''} onChange={handleChange} className="input" placeholder="Qtd portas de alumínio (2F, venezianas)" />

        {/* Janelas */}
        <input name="janelas_basculantes" value={dados.janelas_basculantes || ''} onChange={handleChange} className="input" placeholder="Qtd janelas basculantes" />
        <input name="janelas_maximar" value={dados.janelas_maximar || ''} onChange={handleChange} className="input" placeholder="Qtd janelas maxim-ar" />
        <input name="janelas_outros" value={dados.janelas_outros || ''} onChange={handleChange} className="input" placeholder="Janelas (outros tipos)" />

        {/* Vãos e medidas */}
        <input name="comp_total_vãos" value={dados.comp_total_vãos || ''} onChange={handleChange} className="input" placeholder="Comprimento total dos vãos (m)" />
        <input name="altura_vãos" value={dados.altura_vãos || ''} onChange={handleChange} className="input" placeholder="Altura dos vãos (m)" />
        <input name="peitoril" value={dados.peitoril || ''} onChange={handleChange} className="input" placeholder="Altura do peitoril (cm)" />
        <input name="soleira" value={dados.soleira || ''} onChange={handleChange} className="input" placeholder="Altura da soleira (cm)" />
        <input name="vão_estilob" value={dados.vão_estilob || ''} onChange={handleChange} className="input" placeholder="Qtd de vãos estilo B (profundos)" />
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
