'use client';

import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { authFetch } from '@/src/utils/authFetch';

// Importações das novas etapas
import Etapa1_InfoGeralEndereco from './Etapa1_InfoGeralEndereco';
import Etapa2_CaracteristicasObra from './Etapa2_CaracteristicasObra';
import Etapa3_Financiamento from './Etapa3_Financiamento';
import Etapa4_ServicosPreliminares from './Etapa4_ServicosPreliminares';
import Etapa5_SimulacaoFundacao from './Etapa5_SimulacaoFundacao';

export default function Wizard() {
  const [etapaAtual, setEtapaAtual] = useState(0);
  const [dadosObra, setDadosObra] = useState({});
  const router = useRouter();

  const salvarObra = async () => {
    try {
      const resposta = await authFetch('http://localhost:8000/api/salvar/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dadosObra)
      });

      if (!resposta.ok) throw new Error('Erro ao salvar obra');

      alert('✅ Obra salva com sucesso!');
      router.push('/obras');
    } catch (err) {
      alert('❌ Erro ao salvar obra: ' + err.message);
    }
  };

  const etapas = [
    {
      id: 1,
      componente: (
        <Etapa1_InfoGeralEndereco
          dados={dadosObra}
          setDados={setDadosObra}
          etapaAnterior={() => {}}
          proximaEtapa={() => setEtapaAtual(1)}
        />
      )
    },
    {
      id: 2,
      componente: (
        <Etapa2_CaracteristicasObra
          dados={dadosObra}
          setDados={setDadosObra}
          etapaAnterior={() => setEtapaAtual(0)}
          proximaEtapa={() => setEtapaAtual(2)}
        />
      )
    },
    {
      id: 3,
      componente: (
        <Etapa3_Financiamento
          dados={dadosObra}
          setDados={setDadosObra}
          etapaAnterior={() => setEtapaAtual(1)}
          proximaEtapa={() => setEtapaAtual(3)}
        />
      )
    },
    {
      id: 4,
      componente: (
        <Etapa4_ServicosPreliminares
          dados={dadosObra}
          setDados={setDadosObra}
          etapaAnterior={() => setEtapaAtual(2)}
          proximaEtapa={() => setEtapaAtual(4)}
        />
      )
    },
    {
      id: 5,
      componente: (
        <Etapa5_SimulacaoFundacao
          dados={dadosObra}
          setDados={setDadosObra}
          etapaAnterior={() => setEtapaAtual(3)}
          proximaEtapa={salvarObra}
        />
      )
    }
  ];

  return (
    <div className="w-full max-w-4xl mx-auto p-4 bg-gray-900 text-white rounded-xl shadow-md">
      <AnimatePresence mode="wait">
        <motion.div
          key={etapaAtual}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.4 }}
        >
          {etapas[etapaAtual].componente}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
