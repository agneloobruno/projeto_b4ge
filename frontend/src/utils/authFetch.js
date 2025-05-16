// frontend/src/utils/authFetch.js

export async function authFetch(url, options = {}) {
  const accessToken = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
  };

  let response = await fetch(url, { ...options, headers });

  // Se não autorizado, tenta renovar o token
  if (response.status === 401 && refreshToken) {
    const refreshRes = await fetch("http://localhost:8000/api/auth/token/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (refreshRes.ok) {
      const tokens = await refreshRes.json();
      localStorage.setItem("accessToken", tokens.access);

      // Reenvia a requisição com novo token
      const retryHeaders = {
        ...options.headers,
        Authorization: `Bearer ${tokens.access}`,
      };
      response = await fetch(url, { ...options, headers: retryHeaders });
    } else {
      // Expirou o refresh também — logout
      localStorage.clear();
      window.location.href = "/login";
    }
  }

  return response;
}
