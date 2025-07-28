'use client';

import { useState } from 'react';

export default function Etapa9_Instalacoes({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setDados({ ...dados, [name]: value.replace(',', '.') });
  };

  const validar = () => {
    setErro('');
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
  };

  const parseNumber = (valor) => {
    return valor ? String(valor).replace('.', ',') : '';
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 9 – Instalações</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      {/* Instalações Elétricas */}
      <div className="border rounded p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Instalações Elétricas</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label>
            <span className="text-sm">Eletroduto DN 20mm (1/2") (m)</span>
            <input
              type="text"
              name="eletroduto_20mm"
              value={parseNumber(dados.eletroduto_20mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Eletroduto DN 25mm (3/4") (m)</span>
            <input
              type="text"
              name="eletroduto_25mm"
              value={parseNumber(dados.eletroduto_25mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Fiação de cobre 1,5 mm² (m)</span>
            <input
              type="text"
              name="fio_1_5mm"
              value={parseNumber(dados.fio_1_5mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Fiação de cobre 2,5 mm² (m)</span>
            <input
              type="text"
              name="fio_2_5mm"
              value={parseNumber(dados.fio_2_5mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Cabo 4,0 mm² (m)</span>
            <input
              type="text"
              name="cabo_4mm"
              value={parseNumber(dados.cabo_4mm)}
              onChange={handleChange}
              className="input"
            />
          </label>
        </div>
      </div>

      {/* Instalações Hidrossanitárias */}
      <div className="border rounded p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Instalações Hidrossanitárias</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <label>
            <span className="text-sm">Tubo PVC 20mm (m)</span>
            <input
              type="text"
              name="tubo_pvc_20mm"
              value={parseNumber(dados.tubo_pvc_20mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Tubo PVC 25mm (m)</span>
            <input
              type="text"
              name="tubo_pvc_25mm"
              value={parseNumber(dados.tubo_pvc_25mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Tubo PVC 40mm (m)</span>
            <input
              type="text"
              name="tubo_pvc_40mm"
              value={parseNumber(dados.tubo_pvc_40mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Tubo PVC 50mm (m)</span>
            <input
              type="text"
              name="tubo_pvc_50mm"
              value={parseNumber(dados.tubo_pvc_50mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Tubo PVC 100mm (m)</span>
            <input
              type="text"
              name="tubo_pvc_100mm"
              value={parseNumber(dados.tubo_pvc_100mm)}
              onChange={handleChange}
              className="input"
            />
          </label>

          <label>
            <span className="text-sm">Divisória de Granito (m²)</span>
            <input
              type="text"
              name="divisoria_granito"
              value={parseNumber(dados.divisoria_granito)}
              onChange={handleChange}
              className="input"
            />
          </label>
        </div>
      </div>

      {/* Botões */}
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
