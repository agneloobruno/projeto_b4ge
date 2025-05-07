'use client'

import { useState } from 'react'
import Etapa1 from '@/components/Etapa1'
import Etapa2 from '@/components/Etapa2'
import Etapa3 from '@/components/Etapa3'

export default function Home() {
  const [etapa, setEtapa] = useState(1)
  const [dadosObra, setDadosObra] = useState({
    nome: '',
    tipologia: '',
    localizacao: '',
    areaConstruida: ''
  })

  function proximaEtapa() {
    setEtapa(prev => prev + 1)
  }

  function etapaAnterior() {
    setEtapa(prev => prev - 1)
  }

  function handleChange(e) {
    const { name, value } = e.target
    setDadosObra({ ...dadosObra, [name]: value })
  }

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Cadastro de Obra</h1>

      {etapa === 1 && (
        <Etapa1 dados={dadosObra} onChange={handleChange} proximaEtapa={proximaEtapa} />
      )}
      {etapa === 2 && (
        <Etapa2 etapaAnterior={etapaAnterior} proximaEtapa={proximaEtapa} />
      )}
      {etapa === 3 && (
        <Etapa3 dados={dadosObra} etapaAnterior={etapaAnterior} />
      )}
    </main>
  )
}
