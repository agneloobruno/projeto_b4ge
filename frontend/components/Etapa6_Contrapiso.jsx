'use client';

import { useState } from 'react';

export default function Etapa6_Contrapiso({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value });
  };

  const validar = () => {
    if (!dados.possui_contrapiso) {
      setErro('Informe se há contrapiso.');
      return false;
    }

    if (dados.possui_contrapiso === 'S' && !dados.area_contrapiso) {
      setErro('Informe a área do contrapiso.');
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
      <h2 className="text-2xl font-bold">Etapa 6 – Contrapiso</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <label>
          <span className="text-sm">Possui contrapiso? *</span>
          <select
            name="possui_contrapiso"
            value={dados.possui_contrapiso || ''}
            onChange={handleChange}
            className="input"
          >
            <option value="">Selecione</option>
            <option value="S">Sim</option>
            <option value="N">Não</option>
          </select>
        </label>

        {dados.possui_contrapiso === 'S' && (
          <input
            name="area_contrapiso"
            value={dados.area_contrapiso || ''}
            onChange={handleChange}
            className="input"
            placeholder="Área do contrapiso (m²)"
          />
        )}

        <label>
          <span className="text-sm">Pintura no contrapiso?</span>
          <select
            name="pintura_contrapiso"
            value={dados.pintura_contrapiso || ''}
            onChange={handleChange}
            className="input"
          >
            <option value="">Selecione</option>
            <option value="S">Sim</option>
            <option value="N">Não</option>
          </select>
        </label>
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
