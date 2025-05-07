export default function Etapa1({ dados, onChange, proximaEtapa }) {
    return (
      <div className="space-y-4">
        <div>
          <label>Nome:</label>
          <input name="nome" value={dados.nome} onChange={onChange} className="input" />
        </div>
        <div>
          <label>Tipologia:</label>
          <input name="tipologia" value={dados.tipologia} onChange={onChange} className="input" />
        </div>
        <div>
          <label>Localização:</label>
          <input name="localizacao" value={dados.localizacao} onChange={onChange} className="input" />
        </div>
        <div>
          <label>Área construída (m²):</label>
          <input name="areaConstruida" value={dados.areaConstruida} onChange={onChange} className="input" />
        </div>
        <button onClick={proximaEtapa} className="btn">Próximo</button>
      </div>
    )
  }
  