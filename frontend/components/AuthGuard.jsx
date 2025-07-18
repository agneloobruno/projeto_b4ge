"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthGuard({ children }) {
  const router = useRouter();
  const [verificando, setVerificando] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.replace("/login");
    } else {
      setVerificando(false); // só renderiza os filhos se houver token
    }
  }, [router]);

  if (verificando) {
    return <p className="text-center mt-10">Verificando autenticação...</p>;
  }

  return children;
}
