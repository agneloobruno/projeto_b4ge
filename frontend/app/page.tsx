export default function Page() {
  return (
    <main className="space-y-4">
      <div className="card">
        <p>
          Bem-vindo! Crie uma obra para calcular Energia Embutida e CO₂e,
          ou acesse o resultado de uma obra existente pelo URL <code>/obras/&lt;id&gt;</code>.
        </p>
      </div>
      <div className="card">
        <a className="inline-block px-4 py-2 rounded-xl bg-black text-white dark:bg-white dark:text-black" href="/nova-obra">
          + Nova Obra
        </a>
      </div>
    </main>
  );
}
