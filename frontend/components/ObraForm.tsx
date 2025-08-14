'use client';
import { useEffect, useState } from 'react';
import { getCidades, postObra, type ObraPayload } from '@/lib/api';
import { useRouter } from 'next/navigation';

type Cidade = { id: number; nome: string; estado?: { sigla: string } };

export default function ObraForm() {
  const router = useRouter();
  const [cidades, setCidades] = useState<Cidade[]>([]);
  const [loading, setLoading] = useState(true);
  const [erro, setErro] = useState<string | null>(null);
  const [form, setForm] = useState<ObraPayload>({
    nome: '',
    cidade_id: 1,
    area_construida_m2: '100',
  });

  useEffect(() => {
    (async () => {
      try {
        const list = await getCidades();
        setCidades(list);
      } catch (e: any) {
        setErro(e?.message ?? 'Falha ao carregar cidades');
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  function onChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setForm(prev => ({ ...prev, [name]: name === 'cidade_id' ? Number(value) : value }));
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setErro(null);
    try {
      const obra = await postObra(form);
      router.push(`/obras/${obra.id}`);
    } catch (e: any) {
      setErro(e?.message ?? 'Erro ao salvar');
    }
  }

  return (
    <form onSubmit={onSubmit} className="card space-y-4">
      <h2 className="h2">Nova Obra</h2>
      {erro && <p className="text-red-600 text-sm">{erro}</p>}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <label className="space-y-1">
          <span className="text-sm opacity-80">Nome</span>
          <input name="nome" value={form.nome} onChange={onChange} required className="w-full rounded-xl border px-3 py-2 bg-transparent" />
        </label>
        <label className="space-y-1">
          <span className="text-sm opacity-80">Cidade</span>
          <select name="cidade_id" value={form.cidade_id} onChange={onChange} className="w-full rounded-xl border px-3 py-2 bg-transparent">
            {loading ? <option>Carregando…</option> : cidades.map(c => (
              <option key={c.id} value={c.id}>{c.nome}{c?.estado?.sigla ? ` / ${c.estado.sigla}` : ''}</option>
            ))}
          </select>
        </label>
        <label className="space-y-1">
          <span className="text-sm opacity-80">Área construída (m²)</span>
          <input name="area_construida_m2" value={form.area_construida_m2} onChange={onChange} className="w-full rounded-xl border px-3 py-2 bg-transparent" />
        </label>
      </div>
      <div className="flex gap-3">
        <button className="px-4 py-2 rounded-xl bg-black text-white dark:bg-white dark:text-black">Salvar e ver impactos</button>
        <a href="/" className="px-4 py-2 rounded-xl border">Cancelar</a>
      </div>
    </form>
  );
}
