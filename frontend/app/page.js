'use client';
import Wizard from '../components/Wizard';
import AuthGuard from '../components/AuthGuard';

export default function Home() {
  return (
    <AuthGuard>
      <main className="min-h-screen bg-gray-900 text-white p-8">
        <h1 className="text-3xl font-bold mb-6">Cadastro de Obra</h1>
        <Wizard />
      </main>
    </AuthGuard>
  );
}
