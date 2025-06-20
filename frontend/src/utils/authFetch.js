export async function authFetch(url, options = {}) {
  const accessToken = localStorage.getItem("accessToken");
  const refreshToken = localStorage.getItem("refreshToken");

  const headers = {
    ...options.headers,
    Authorization: `Bearer ${accessToken}`,
    "Content-Type": "application/json", // 🔧 Incluído também aqui
  };

  let response = await fetch(url, { ...options, headers });

  if (response.status === 401 && refreshToken) {
    const refreshRes = await fetch("http://localhost:8000/api/auth/token/refresh/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    if (refreshRes.ok) {
      const tokens = await refreshRes.json();
      localStorage.setItem("accessToken", tokens.access);

      const retryHeaders = {
        ...options.headers,
        Authorization: `Bearer ${tokens.access}`,
        "Content-Type": "application/json", // 🔧 Aqui também
      };

      response = await fetch(url, { ...options, headers: retryHeaders });
    } else {
      localStorage.clear();
      window.location.href = "/login";
    }
  }

  return response;
}
