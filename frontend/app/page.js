'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      router.replace('/obras'); // só vai para obras se estiver logado
    } else {
      router.replace('/login'); // se não estiver logado, vai pro login
    }
  }, []);

  return null;
}
