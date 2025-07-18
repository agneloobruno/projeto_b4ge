"use client";

import ImpactoResumo from "@/components/ImpactoResumo";
import { useParams } from "next/navigation";

export default function ObraDetalhePage() {
  const params = useParams();
  const obraId = params?.id;

  if (!obraId) return <p>Obra não encontrada.</p>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Detalhes da Obra #{obraId}</h1>
      <ImpactoResumo obraId={obraId} />
    </div>
  );
}
