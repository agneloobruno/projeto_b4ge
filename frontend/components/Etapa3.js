export default function Etapa3({ dados, etapaAnterior }) {
    function handleSubmit() {
      fetch('http://localhost:8000/api/obras/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dados),
      })
        .then(res => res.json())
        .then(data => alert('Obra cadastrada com sucesso!'))
        .catch(err => alert('Erro ao enviar!'))
    }
  
    return (
      <div>
        <h2 className="text-xl font-bold mb-4">Resumo</h2>
        <pre className="bg-gray-800 p-4 rounded">{JSON.stringify(dados, null, 2)}</pre>
        <button onClick={etapaAnterior} className="btn mr-2">Voltar</button>
        <button onClick={handleSubmit} className="btn bg-green-600 hover:bg-green-700">Enviar</button>
      </div>
    )
  }
  