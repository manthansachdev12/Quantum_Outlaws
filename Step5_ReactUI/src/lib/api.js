const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || `Request failed with status ${response.status}`);
  }

  return data;
}

export const api = {
  base: API_BASE,
  health: () => request("/health"),
  baseline: () => request("/baseline"),
  results: (limit = 20) => request(`/results?limit=${limit}`),
  verify: (payload) =>
    request("/verify", { method: "POST", body: JSON.stringify(payload) }),
  channel: (payload) =>
    request("/attack/channel", { method: "POST", body: JSON.stringify(payload) }),
  forgery: (payload) =>
    request("/attack/forgery", { method: "POST", body: JSON.stringify(payload) }),
  impersonation: (payload) =>
    request("/attack/impersonation", { method: "POST", body: JSON.stringify(payload) }),
  replay: (payload) =>
    request("/attack/replay", { method: "POST", body: JSON.stringify(payload) }),
};
