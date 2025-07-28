'use client';

import { useState } from 'react';

export default function Etapa7_Esquadrias({ dados, setDados, etapaAnterior, proximaEtapa }) {
  const [erro, setErro] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Se for número com vírgula, normaliza para ponto para salvar corretamente
    const normalizado = value.replace(',', '.');

    setDados({ ...dados, [name]: normalizado });
  };

  const validar = () => {
    // Nenhum campo obrigatório por padrão
    return true;
  };

  const handleAvancar = () => {
    if (validar()) proximaEtapa();
    else setErro('Verifique os campos preenchidos.');
  };

  // Helper para exibir vírgula no input
  const formatar = (valor) => {
    return (valor || '').toString().replace('.', ',');
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Etapa 7 – Esquadrias</h2>
      {erro && <p className="text-sm text-red-400">{erro}</p>}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* PORTAS */}
        <fieldset className="border p-4 rounded-md space-y-4">
          <legend className="text-sm font-semibold">Portas</legend>

          <label>
            <span className="text-sm">Porta de madeira 60 x 210 cm (und)</span>
            <input name="porta_madeira_60x210" value={formatar(dados.porta_madeira_60x210)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de madeira 70 x 210 cm (und)</span>
            <input name="porta_madeira_70x210" value={formatar(dados.porta_madeira_70x210)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de madeira 80 x 210 cm (und)</span>
            <input name="porta_madeira_80x210" value={formatar(dados.porta_madeira_80x210)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de madeira 120 x 210 cm 2F (und)</span>
            <input name="porta_madeira_120x210_2f" value={formatar(dados.porta_madeira_120x210_2f)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de alumínio de abrir 1F (m²)</span>
            <input name="porta_aluminio_1f" value={formatar(dados.porta_aluminio_1f)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de correr de alumínio 2F (m²)</span>
            <input name="porta_aluminio_2f" value={formatar(dados.porta_aluminio_2f)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Porta de alumínio veneziana (m²)</span>
            <input name="porta_veneziana" value={formatar(dados.porta_veneziana)} onChange={handleChange} className="input" />
          </label>
        </fieldset>

        {/* JANELAS */}
        <fieldset className="border p-4 rounded-md space-y-4">
          <legend className="text-sm font-semibold">Janelas</legend>

          <label>
            <span className="text-sm">Área total de janela basculante de aço (m²)</span>
            <input name="janela_basculante" value={formatar(dados.janela_basculante)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Área total de janela correr de alumínio 2 folhas 100x120cm (m²)</span>
            <input name="janela_correr_2f_100x120" value={formatar(dados.janela_correr_2f_100x120)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Área total de janela de alumínio Maxim-Ar (m²)</span>
            <input name="janela_maximar" value={formatar(dados.janela_maximar)} onChange={handleChange} className="input" />
          </label>
        </fieldset>

        {/* OUTROS ELEMENTOS */}
        <fieldset className="md:col-span-2 border p-4 rounded-md space-y-4">
          <legend className="text-sm font-semibold">Outros elementos</legend>

          <label>
            <span className="text-sm">Comprimento das vergas (total) (m)</span>
            <input name="comprimento_vergas" value={formatar(dados.comprimento_vergas)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Peitoril linear de granito ou mármore (m)</span>
            <input name="peitoril_granito" value={formatar(dados.peitoril_granito)} onChange={handleChange} className="input" />
          </label>

          <label>
            <span className="text-sm">Brise em chapa metálica perfurada (m²)</span>
            <input name="brise_chapa" value={formatar(dados.brise_chapa)} onChange={handleChange} className="input" />
          </label>
        </fieldset>
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
