const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
const TOKEN_KEY = "signaldesk_access_token";

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function storeToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request(path, { token, ...options } = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  const isJson = response.headers.get("content-type")?.includes("application/json");
  const payload = isJson ? await response.json() : await response.text();

  if (!response.ok) {
    const message = payload?.error?.message || payload?.detail?.[0]?.msg || "Request failed";
    throw new Error(message);
  }

  return payload;
}

export const api = {
  login(credentials) {
    return request("/auth/login", {
      method: "POST",
      body: JSON.stringify(credentials),
    });
  },
  dashboard(token) {
    return request("/analytics/dashboard", { token });
  },
  leads(token) {
    return request("/leads", { token });
  },
  conversations(token) {
    return request("/conversations", { token });
  },
  workflows(token) {
    return request("/workflows", { token });
  },
  createWorkflow(token, payload) {
    return request("/workflows", {
      token,
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  integrations(token) {
    return request("/integrations", { token });
  },
  botConfig(token) {
    return request("/bot-config", { token });
  },
  updateBotConfig(token, payload) {
    return request("/bot-config", {
      token,
      method: "PUT",
      body: JSON.stringify(payload),
    });
  },
  resetDemo(token) {
    return request("/demo/reset", {
      token,
      method: "POST",
    });
  },
  simulateWhatsApp(token, payload) {
    return request("/whatsapp/simulate", {
      token,
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  sendConversationMessage(token, payload) {
    return request("/conversations/messages", {
      token,
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  sendInteractiveReply(token, payload) {
    return request("/whatsapp/interactive-reply", {
      token,
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
};
