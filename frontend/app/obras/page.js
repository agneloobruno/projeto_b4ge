'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

export default function ObrasPage() {
  const [obras, setObras] = useState([])
  const [carregando, setCarregando] = useState(true)

  useEffect(() => {
    fetch('http://localhost:8000/api/obras/')
      .then((res) => res.json())
      .then((data) => {
        setObras(data)
        setCarregando(false)
      })
      .catch(() => setCarregando(false))
  }, [])

  return (
    <main className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Obras Cadastradas</h1>

      <Link href="/" className="text-blue-400 underline mb-6 inline-block">
        Voltar para cadastro
      </Link>

      {carregando ? (
        <p>Carregando obras...</p>
      ) : obras.length === 0 ? (
        <p>Nenhuma obra cadastrada.</p>
      ) : (
        <div className="space-y-4">
          {obras.map((obra) => (
            <div
              key={obra.id}
              className="bg-gray-800 p-4 rounded shadow-md border border-gray-700"
            >
              <p><strong>Nome:</strong> {obra.nome}</p>
              <p><strong>Tipologia:</strong> {obra.tipologia}</p>
              <p><strong>Localização:</strong> {obra.localizacao}</p>
              <p><strong>Área construída:</strong> {obra.area_construida} m²</p>
              {obra.energia_embutida_total && (
                <p><strong>Energia:</strong> {obra.energia_embutida_total} MJ</p>
              )}
              {obra.co2_total && (
                <p><strong>CO₂:</strong> {obra.co2_total} kg</p>
              )}
            </div>
          ))}
        </div>
      )}
    </main>
  )
}
