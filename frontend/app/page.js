'use client'

import { useEffect, useState } from 'react'

export default function Home() {
  const [resposta, setResposta] = useState(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/ping/')
      .then((res) => res.json())
      .then((data) => setResposta(data.message))
  }, [])

  return (
    <main className="min-h-screen bg-gray-900 text-white p-10">
      <h1 className="text-4xl font-bold">Conexão com Django</h1>
      <p className="mt-4 text-xl">{resposta || 'Conectando...'}</p>
    </main>
  )
}
