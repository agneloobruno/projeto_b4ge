'use client';

import { useState } from 'react';

const TIPOS_PISO = [
  'Cerâmico',
  'Porcelanato',
  'Vinílico',
  'Laminado',
  'Madeira',
  'Cimento queimado',
  'Granilite',
  'Outro'
];

export default function Etapa8_Revestimentos({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    const normalizado = value.replace(',', '.');
    setDados({ ...dados, [name]: normalizado });

    if (erro) setErro('');
  };

  const validar = () => {
    if (!dados.tipologia_piso || !dados.area_revestimento) {
      setErro('Preencha a tipologia e área de revestimento.');
      return false;
    }
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
  };

  const formatar = (valor) => {
    return (valor || '').toString().replace('.', ',');
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 8 – Revestimentos</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="border rounded p-4 shadow-sm">
        <h3 className="text-lg font-semibold mb-2">Revestimentos e acabamentos</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

          <label>
            <span className="text-sm">Tipologia de piso *</span>
            <select
              name="tipologia_piso"
              value={dados.tipologia_piso || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione</option>
              {TIPOS_PISO.map((tipo) => (
                <option key={tipo} value={tipo}>{tipo}</option>
              ))}
            </select>
          </label>

          <label>
            <span className="text-sm">Área de revestimento cerâmico de parede (m²) *</span>
            <input
              name="area_revestimento"
              value={formatar(dados.area_revestimento)}
              onChange={handleChange}
              className="input"
              placeholder="Ex: 123,45"
            />
          </label>

          <label>
            <span className="text-sm">Possui pintura externa?</span>
            <select
              name="pintura_externa"
              value={dados.pintura_externa || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione</option>
              <option value="S">Sim</option>
              <option value="N">Não</option>
            </select>
          </label>

          <label>
            <span className="text-sm">Possui pintura interna?</span>
            <select
              name="pintura_interna"
              value={dados.pintura_interna || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione</option>
              <option value="S">Sim</option>
              <option value="N">Não</option>
            </select>
          </label>

          <label>
            <span className="text-sm">Possui placa de gesso acartonado?</span>
            <select
              name="gesso"
              value={dados.gesso || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione</option>
              <option value="Simples">Simples</option>
              <option value="Duplo">Duplo</option>
              <option value="N">Não</option>
            </select>
          </label>

          <label>
            <span className="text-sm">Possui esquadrias de madeira?</span>
            <select
              name="esquadrias_madeira"
              value={dados.esquadrias_madeira || ''}
              onChange={handleChange}
              className="input"
            >
              <option value="">Selecione</option>
              <option value="S">Sim</option>
              <option value="N">Não</option>
            </select>
          </label>

          <label>
            <span className="text-sm">Soleira de mármore (m)</span>
            <input
              name="soleira"
              value={formatar(dados.soleira)}
              onChange={handleChange}
              className="input"
              placeholder="Ex: 3,20"
            />
          </label>

          <label>
            <span className="text-sm">Rodapé de granito (m)</span>
            <input
              name="rodape"
              value={formatar(dados.rodape)}
              onChange={handleChange}
              className="input"
              placeholder="Ex: 4,80"
            />
          </label>

        </div>
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
