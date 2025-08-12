// frontend/components/Wizard.jsx
'use client';

import { useState, useRef } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { useRouter } from 'next/navigation';
import { authFetch } from '@/src/utils/authFetch';
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

const ETAPAS = [
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

const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Normaliza “1.234,56” -> 1234.56, strings vazias -> null
function normalizarNumero(v) {
  if (v === null || v === undefined || v === '') return null;
  if (typeof v === 'number') return Number.isFinite(v) ? v : null;
  const s = String(v).replace(/\./g, '').replace(',', '.');
  const n = Number(s);
  return Number.isFinite(n) ? n : null;
}

// Ajuste esta função para refletir exatamente como cada etapa salva no `dadosObra`.
// A ideia é transformar o estado do wizard em uma lista plana de itens.
function coletarItensDoWizard(dados) {
  const itens = [];

  // Exemplos (substitua pelos seus nomes reais):
  // FUNDACAO
  if (Array.isArray(dados.fundacao_materiais)) {
    dados.fundacao_materiais.forEach(m => {
      itens.push({
        etapa_obra: 'FUNDACAO',
        // use um dos dois: insumo_id (se já vem do banco) OU codigo_sinapi
        insumo_id: m.insumo_id ?? null,
        codigo_sinapi: m.codigo_sinapi ?? null,
        quantidade: normalizarNumero(m.quantidade),
        unidade: m.unidade ?? 'kg',
        proporcao: normalizarNumero(m.proporcao),
        distancia_km: normalizarNumero(m.distancia_km)
      });
    });
  }

  // ESTRUTURA
  if (Array.isArray(dados.estrutura_materiais)) {
    dados.estrutura_materiais.forEach(m => {
      itens.push({
        etapa_obra: 'ESTRUTURA',
        insumo_id: m.insumo_id ?? null,
        codigo_sinapi: m.codigo_sinapi ?? null,
        quantidade: normalizarNumero(m.quantidade),
        unidade: m.unidade ?? 'kg',
        proporcao: normalizarNumero(m.proporcao),
        distancia_km: normalizarNumero(m.distancia_km)
      });
    });
  }

  // Repita para as demais etapas (VEDACOES, COBERTURA, etc.)
  // ...

  // Remova itens sem quantidade válida
  return itens.filter(i => i.quantidade !== null && i.quantidade > 0);
}

// Escolha explicitamente quais campos gerais vão para a criação da Obra
function prepararPayloadObra(dados) {
  return {
    nome: dados.nome ?? '',
    tipologia: dados.tipologia ?? '',
    cep: dados.cep ?? '',
    estado: dados.estado ?? '',
    cidade_id: dados.cidade ?? null,     // cuidado: back espera *_id?
    area_construida: normalizarNumero(dados.area_construida),
    // ... adicione somente o que o backend espera para criar a Obra
    // (não envie campos calculados como energia_* ou co2_*)
    usuario: typeof window !== 'undefined' ? localStorage.getItem('userId') : null
  };
}

export default function Wizard() {
  const [etapaAtual, setEtapaAtual] = useState(0);
  const [dadosObra, setDadosObra] = useState({});
  const salvandoRef = useRef(false);
  const router = useRouter();
  const EtapaAtual = ETAPAS[etapaAtual].componente;

  const salvarObra = async () => {
    if (salvandoRef.current) return;
    salvandoRef.current = true;

    const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null;
    if (!token) {
      alert('⚠️ Você precisa estar logado para salvar uma obra.');
      salvandoRef.current = false;
      router.push('/login');
      return;
    }

    try {
      // 1) Cria a obra
      const obraPayload = prepararPayloadObra(dadosObra);
      console.log('[DEBUG] Payload obra:', obraPayload);

      const respObra = await authFetch(`${base}/api/obras/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(obraPayload)
      });

      const obraJson = await respObra.json();
      if (!respObra.ok) {
        throw new Error(obraJson?.detail || JSON.stringify(obraJson));
      }
      const id = obraJson?.id;
      if (!id) {
        throw new Error('Backend não retornou o ID da obra criada.');
      }

      // 2) Monta e envia itens (wizard -> InsumoAplicado)
      const itens = coletarItensDoWizard(dadosObra);
      console.log('[DEBUG] Itens coletados:', itens);

      if (itens.length > 0) {
        const respItens = await authFetch(`${base}/api/obras/${id}/adicionar_itens/`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ itens })
        });
        const itensJson = await respItens.json();
        if (!respItens.ok) {
          throw new Error(itensJson?.detail || JSON.stringify(itensJson));
        }
      } else {
        console.warn('Nenhum item coletado do wizard – impactos podem ficar zerados.');
      }

      // 3) (Opcional) força recálculo no backend
      try {
        await authFetch(`${base}/api/obras/${id}/atualizar_impacto/`, { method: 'POST' });
      } catch (e) {
        console.warn('Falha ao chamar /atualizar_impacto – seguindo adiante.', e);
      }

      // 4) Busca o resumo para exibir ou armazenar em estado/contexto
      try {
        const r = await authFetch(`${base}/api/impactos/obra/${id}/`);
        const resumo = await r.json();
        console.log('[DEBUG] Resumo de impactos:', resumo);
        // aqui você pode salvar em um estado global/contexto, ou
        // enviar para a página de detalhes da obra com querystring/state
      } catch (e) {
        console.warn('Falha ao buscar resumo de impactos.', e);
      }

      alert('✅ Obra salva com sucesso!');
      // Navegue só no final do fluxo
      router.push('/obras');
      return; // encerra a função
    } catch (err) {
      console.error(err);
      alert('❌ Erro ao salvar obra: ' + err.message);
    } finally {
      salvandoRef.current = false;
    }
  };

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
              if (etapaAtual < ETAPAS.length - 1) {
                setEtapaAtual(etapaAtual + 1);
              } else {
                salvarObra();
              }
            }}
          />
        </motion.div>
      </AnimatePresence>

      <div className="text-center text-sm text-gray-400 mt-4">
        Etapa {etapaAtual + 1} de {ETAPAS.length}
      </div>
    </div>
  );
}
