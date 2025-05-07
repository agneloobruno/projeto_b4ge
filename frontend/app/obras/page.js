// app/obras/page.js
"use client";

import { useEffect, useState } from "react";
import ObraForm from "@/components/ObraForm";
import ObraResumo from "@/components/ObraResumo";

export default function ObrasPage() {
  const [obras, setObras] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/obras/")
      .then((res) => res.json())
      .then((data) => setObras(data));
  }, []);

  const adicionarObra = (novaObra) => {
    fetch("http://localhost:8000/api/obras/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(novaObra),
    })
      .then((res) => res.json())
      .then((data) => setObras((prev) => [...prev, data]));
  };

  return (
    <main className="p-4">
      <h1 className="text-3xl font-bold mb-4">Obras cadastradas</h1>
      <div className="flex flex-col md:flex-row gap-4">
        <div className="w-full md:w-1/2">
          <ObraForm onSubmit={adicionarObra} />
        </div>
        <div className="w-full md:w-1/2">
          <ObraResumo obras={obras} />
        </div>
      </div>
    </main>
  );
}
