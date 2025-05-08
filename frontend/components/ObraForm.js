"use client";

import { useState } from "react";

export default function ObraForm({ onSubmit }) {
  const [nome, setNome] = useState("");
  const [tipologia, setTipologia] = useState("");
  const [localizacao, setLocalizacao] = useState("");
  const [area_construida, setAreaConstruida] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // 🔥 Aqui montamos o objeto final com os nomes certos
    const novaObra = {
      nome: nome,
      tipologia: tipologia,
      localizacao: localizacao,
      area_construida: parseFloat(area_construida), // snake_case correto
    };

    console.log("📦 Obra enviada:", novaObra); // CONFIRA isso no console
    onSubmit(novaObra);

    setNome("");
    setTipologia("");
    setLocalizacao("");
    setAreaConstruida("");
    alert("Obra cadastrada com sucesso!");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input value={nome} onChange={(e) => setNome(e.target.value)} placeholder="Nome" className="w-full p-2 border rounded" required />
      <input value={tipologia} onChange={(e) => setTipologia(e.target.value)} placeholder="Tipologia" className="w-full p-2 border rounded" required />
      <input value={localizacao} onChange={(e) => setLocalizacao(e.target.value)} placeholder="Localização" className="w-full p-2 border rounded" required />
      <input type="number" value={areaConstruida} onChange={(e) => setAreaConstruida(e.target.value)} placeholder="Área construída (m²)" className="w-full p-2 border rounded" required />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Cadastrar</button>
    </form>
  );
}
