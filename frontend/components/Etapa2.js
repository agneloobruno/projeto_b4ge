export default function Etapa2({ etapaAnterior, proximaEtapa }) {
    return (
      <div>
        <p className="mb-4">[mock] Seleção de materiais (em breve)</p>
        <button onClick={etapaAnterior} className="btn mr-2">Voltar</button>
        <button onClick={proximaEtapa} className="btn">Próximo</button>
      </div>
    )
  }
  