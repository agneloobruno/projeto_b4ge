// frontend/components/Wizard.jsx
'use client';

import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { authFetch } from '@/src/utils/authFetch';

// Importações das 10 etapas verdadeiras
import Etapa1 from './Etapa1_InformacoesGerais';
import Etapa2 from './Etapa2_Fundacao';
import Etapa3 from './Etapa3_Superestrutura';
import Etapa4 from './Etapa4_Vedacoes';
import Etapa5 from './Etapa5_Cobertura';
import Etapa6 from './Etapa6_Contrapiso';
import Etapa7 from './Etapa7_Esquadrias';
import Etapa8 from './Etapa8_Revestimentos';
import Etapa9 from './Etapa9_Instalacoes';
import Etapa10 from './Etapa10_MaoDeObraUsuarios';

export default function Wizard() {
  const [etapaAtual, setEtapaAtual] = useState(0);
  const [dadosObra, setDadosObra] = useState({});
  const router = useRouter();

  // Função de salvar obra ajustada para usar o endpoint correto e o token via authFetch
  const salvarObra = async () => {
    try {
      const resposta = await authFetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/obras/`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(dadosObra)
        }
      );

      if (!resposta.ok) {
        throw new Error(`Erro ao salvar obra: ${resposta.status} ${resposta.statusText}`);
      }

      alert('✅ Obra salva com sucesso!');
      router.push('/obras');
    } catch (err) {
      alert('❌ Erro ao salvar obra: ' + err.message);
    }
  };

  const etapas = [
    { id: 1, componente: Etapa1 },
    { id: 2, componente: Etapa2 },
    { id: 3, componente: Etapa3 },
    { id: 4, componente: Etapa4 },
    { id: 5, componente: Etapa5 },
    { id: 6, componente: Etapa6 },
    { id: 7, componente: Etapa7 },
    { id: 8, componente: Etapa8 },
    { id: 9, componente: Etapa9 },
    { id: 10, componente: Etapa10 }
  ];
  const EtapaAtual = etapas[etapaAtual].componente;

  return (
    <div className="w-full max-w-5xl mx-auto p-6 bg-gray-900 text-white rounded-xl shadow-md">
      <h1 className="text-3xl font-bold mb-4">Cadastro de Obra</h1>

      <AnimatePresence mode="wait">
        <motion.div
          key={etapaAtual}
          initial={{ opacity: 0, x: 100 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -100 }}
          transition={{ duration: 0.4 }}
        >
          <EtapaAtual
            dados={dadosObra}
            setDados={setDadosObra}
            etapaAnterior={() => etapaAtual > 0 && setEtapaAtual(etapaAtual - 1)}
            proximaEtapa={() => {
              if (etapaAtual < etapas.length - 1) {
                setEtapaAtual(etapaAtual + 1);
              } else {
                salvarObra();
              }
            }}
          />
        </motion.div>
      </AnimatePresence>

      <div className="text-center text-sm text-gray-400 mt-4">
        Etapa {etapaAtual + 1} de {etapas.length}
      </div>
    </div>
  );
}
