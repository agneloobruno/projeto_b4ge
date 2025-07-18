"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function AuthGuard({ children }) {
  const router = useRouter();
  const [verificando, setVerificando] = useState(true);

  useEffect(() => {
    const token = typeof window !== "undefined" && localStorage.getItem("accessToken");

    if (!token) {
      router.replace("/login");
    } else {
      setVerificando(false);
    }
  }, [router]);

  if (verificando) return <p>Verificando autenticação...</p>;

  return children;
}
