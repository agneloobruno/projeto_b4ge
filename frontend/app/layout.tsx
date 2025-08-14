export const metadata = {
  title: "B4GE – Calculadora",
  description: "Calculadora de CO₂e e Energia Embutida",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>
        <div className="container py-6 space-y-6">
          <header className="flex items-center justify-between">
            <h1 className="h1">B4GE – Calculadora</h1>
            <nav className="text-sm opacity-80 space-x-4">
              <a href="/" className="hover:underline">Início</a>
              <a href="/nova-obra" className="hover:underline">Nova Obra</a>
            </nav>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
