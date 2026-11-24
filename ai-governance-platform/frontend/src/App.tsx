import { useEffect, useState } from "react";
import { request, token } from "./api";
type User = { id:number; full_name:string; email:string; role:string };
type Model = { id:number; name:string; version:string; provider:string; use_case:string; lifecycle_status:string; risk_level:string };
export default function App() {
  const [loggedIn,setLoggedIn] = useState(!!token());
  const [user,setUser] = useState<User|null>(null);
  const [models,setModels] = useState<Model[]>([]);
  const [error,setError] = useState("");
  const [busy,setBusy] = useState(false);
  async function refresh() {
    try { setUser(await request<User>("/auth/me")); setModels(await request<Model[]>("/models")); setError(""); }
    catch(e) { setError(e instanceof Error ? e.message : "Unable to load data"); }
  }
  useEffect(() => { if(loggedIn) void refresh(); }, [loggedIn]);
  async function login(e:React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); setBusy(true); setError("");
    const f = new FormData(e.currentTarget);
    try {
      const r = await request<{access_token:string}>("/auth/login",{method:"POST",body:JSON.stringify({email:f.get("email"),password:f.get("password")})});
      localStorage.setItem("access_token",r.access_token); setLoggedIn(true);
    } catch(err) { setError(err instanceof Error ? err.message : "Login failed"); }
    finally { setBusy(false); }
  }
  async function addModel(e:React.FormEvent<HTMLFormElement>) {
    e.preventDefault(); setBusy(true); setError("");
    const f = new FormData(e.currentTarget);
    try {
      await request("/models",{method:"POST",body:JSON.stringify({name:f.get("name"),version:f.get("version"),provider:f.get("provider") || "Not specified",use_case:f.get("use_case")})});
      e.currentTarget.reset(); await refresh();
    } catch(err) { setError(err instanceof Error ? err.message : "Could not save model"); }
    finally { setBusy(false); }
  }
  function logout() { localStorage.removeItem("access_token"); setLoggedIn(false); setUser(null); setModels([]); }
  if(!loggedIn) return <main className="login"><section className="panel">
    <p className="eyebrow">MODEL RISK · GOVERNANCE · OVERSIGHT</p><h1>AI Governance Platform</h1>
    <p className="muted">Sign in to manage AI model inventory and risk.</p>
    <form className="stack" onSubmit={login}><label>Email<input name="email" type="email" required /></label>
    <label>Password<input name="password" type="password" required /></label><button disabled={busy}>{busy?"Signing in...":"Sign in"}</button></form>
    <p className="muted small">First create an account using POST /api/v1/auth/register in the backend API docs.</p>{error && <p className="error">{error}</p>}
  </section></main>;
  return <main className="shell"><header className="topbar"><div><p className="eyebrow">GOVERNANCE WORKSPACE</p><h1>AI Risk Overview</h1></div>
    <div className="user">{user?.full_name} · {user?.role}<button className="secondary" onClick={logout}>Sign out</button></div></header>
    {error && <p className="error">{error}</p>}
    <section className="stats"><article className="stat"><span>Registered models</span><strong>{models.length}</strong></article>
    <article className="stat"><span>In development</span><strong>{models.filter(m=>m.lifecycle_status==="development").length}</strong></article>
    <article className="stat"><span>High / critical risk</span><strong>{models.filter(m=>["high","critical"].includes(m.risk_level)).length}</strong></article></section>
    <section className="panel"><h2>Register an AI model</h2><form className="model-form" onSubmit={addModel}>
      <label>Model name<input name="name" required minLength={2} placeholder="Customer Support Classifier"/></label>
      <label>Version<input name="version" required placeholder="1.0.0"/></label>
      <label>Provider<input name="provider" placeholder="Internal / vendor"/></label>
      <label className="wide">Use case<textarea name="use_case" required minLength={10} placeholder="Describe intended use, users and decision context."/></label>
      <button disabled={busy}>{busy?"Saving...":"Register model"}</button></form></section>
    <section className="panel"><div className="section-heading"><div><h2>Model inventory</h2><p className="muted">Registered AI systems</p></div><button className="secondary" onClick={()=>void refresh()}>Refresh</button></div>
    <div className="table-wrap"><table><thead><tr><th>Model</th><th>Version</th><th>Provider</th><th>Lifecycle</th><th>Risk</th></tr></thead><tbody>
    {models.map(m=><tr key={m.id}><td>{m.name}</td><td>{m.version}</td><td>{m.provider}</td><td>{m.lifecycle_status}</td><td><span className={`pill ${m.risk_level}`}>{m.risk_level}</span></td></tr>)}
    {!models.length && <tr><td colSpan={5} className="empty">No models registered yet.</td></tr>}</tbody></table></div></section>
    <p className="footer">Development starter · Risk score is illustrative, not a validated regulatory methodology.</p></main>;
}