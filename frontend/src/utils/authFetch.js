// src/utils/authFetch.js

export async function authFetch(url, options = {}) {
  // Lê sempre das mesmas chaves
  const accessToken  = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");

  // Cabeçalhos padrão com token de acesso
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json",
  };

  // Primeiro fetch com o token atual
  let response = await fetch(url, { ...options, headers });

  // Se der 401 (token expirado) e existir refreshToken, tenta renovar
  if (response.status === 401 && refreshToken) {
    const refreshRes = await fetch(
      `${process.env.NEXT_PUBLIC_API_URL}/api/token/refresh/`, // endpoint correto
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh: refreshToken }),
      }
    );

    if (refreshRes.ok) {
      // Se o refresh funcionou, atualiza ambos os tokens
      const tokens = await refreshRes.json();
      localStorage.setItem("accessToken", tokens.access);
      localStorage.setItem("refreshToken", tokens.refresh);

      // E refaz a requisição original com o novo accessToken
      const retryHeaders = {
        ...options.headers,
        Authorization: `Bearer ${tokens.access}`,
        "Content-Type": "application/json",
      };
      response = await fetch(url, { ...options, headers: retryHeaders });
    } else {
      // Se o refresh também falhar, limpa o storage e força logout
      localStorage.clear();
      window.location.href = "/login";
    }
  }

  return response;
}
