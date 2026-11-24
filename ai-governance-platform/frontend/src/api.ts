const API = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000/api/v1";
export function token() { return localStorage.getItem("access_token"); }
export async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const t = token();
  const res = await fetch(`${API}${path}`, { ...options, headers: {
    "Content-Type": "application/json", ...(t ? { Authorization: `Bearer ${t}` } : {}), ...options.headers
  }});
  if (!res.ok) { const body = await res.json().catch(() => ({})); throw new Error(body.detail ?? `HTTP ${res.status}`); }
  return res.json() as Promise<T>;
}