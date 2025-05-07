"use client";

import { useState } from "react";

export default function ObraForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    nome: "",
    tipologia: "",
    localizacao: "",
    area_construida: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const dadosCorrigidos = {
      ...formData,
      area_construida: parseFloat(formData.area_construida),
    };
    onSubmit(dadosCorrigidos);
    setFormData({
      nome: "",
      tipologia: "",
      localizacao: "",
      area_construida: "",
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <input name="nome" value={formData.nome} onChange={handleChange} placeholder="Nome" className="w-full p-2 border rounded" required />
      <input name="tipologia" value={formData.tipologia} onChange={handleChange} placeholder="Tipologia" className="w-full p-2 border rounded" required />
      <input name="localizacao" value={formData.localizacao} onChange={handleChange} placeholder="Localização" className="w-full p-2 border rounded" required />
      <input name="area_construida" type="number" value={formData.area_construida} onChange={handleChange} placeholder="Área construída (m²)" className="w-full p-2 border rounded" required />
      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">Cadastrar</button>
    </form>
  );
}
