"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginForm() {
  const router = useRouter();
  const [cpf, setCpf] = useState("");
  const [senha, setSenha] = useState("");
  const [erro, setErro] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const resposta = await fetch("http://localhost:8000/api/token/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: cpf, password: senha }),
      });

      if (!resposta.ok) throw new Error("Credenciais inválidas");

      const dados = await resposta.json();

      // Salva os tokens com chaves consistentes
      localStorage.setItem("accessToken", dados.access);
      localStorage.setItem("refreshToken", dados.refresh);

      router.push("/obras");
    } catch (err) {
      setErro(err.message);
    }
  };

  return (
    <form onSubmit={handleLogin} className="space-y-4 max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold text-center">Login</h2>
      {erro && <p className="text-red-500 text-sm">{erro}</p>}

      <input
        type="text"
        placeholder="CPF"
        value={cpf}
        onChange={(e) => setCpf(e.target.value)}
        className="w-full border border-gray-400 px-3 py-2 rounded"
      />
      <input
        type="password"
        placeholder="Senha"
        value={senha}
        onChange={(e) => setSenha(e.target.value)}
        className="w-full border border-gray-400 px-3 py-2 rounded"
      />
      <button
        type="submit"
        className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700"
      >
        Entrar
      </button>
    </form>
  );
}
