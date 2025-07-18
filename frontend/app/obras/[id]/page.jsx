"use client";
import ImpactoResumo from "@/components/ImpactoResumo";
import { useParams }  from "next/navigation" ;
import AuthGuard      from "@/components/AuthGuard";

export default function ObraDetalhePage() {
  const params = useParams();
  const obraId = params?.id;

  console.log("🚀 ObraDetalhePage → obraId =", obraId);

  if (!obraId) return <p>Obra não encontrada.</p>;

  return (
    <AuthGuard>
      <div className="p-6">
        <h1>Detalhes da Obra #{obraId}</h1>
        <ImpactoResumo obraId={obraId} />
      </div>
    </AuthGuard>
  );
}
