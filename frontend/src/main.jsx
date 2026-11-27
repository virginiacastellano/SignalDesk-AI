import React, { useEffect, useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  BarChart3,
  Bot,
  BrainCircuit,
  CheckCircle2,
  Clock3,
  ContactRound,
  Gauge,
  Inbox,
  Loader2,
  LogOut,
  MessageCircle,
  PlugZap,
  Send,
  ShieldCheck,
  Sparkles,
  Tags,
  Workflow,
  X,
} from "lucide-react";
import { timeline } from "./data/demo";
import { api, clearToken, getStoredToken, storeToken } from "./lib/api";
import "./styles.css";

const demoCredentials = {
  email: "founder@novagrowth.io",
  password: "Password123!",
};

const simulationPresets = [
  { label: "Menu", phone: "+5491122334401", message: "Hola" },
  { label: "Precios", phone: "+5491122334402", message: "Hola, quiero saber precios" },
  { label: "Handoff", phone: "+5491122334403", message: "Necesito hablar con un asesor" },
  { label: "Ecommerce", phone: "+5491122334404", message: "Quiero automatizar consultas de mi ecommerce" },
];

function formatNumber(value) {
  return new Intl.NumberFormat("en-US").format(value ?? 0);
}

function formatRelative(dateValue) {
  if (!dateValue) return "now";
  const date = new Date(dateValue);
  const diffMinutes = Math.max(1, Math.round((Date.now() - date.getTime()) / 60000));
  if (diffMinutes < 60) return `${diffMinutes}m`;
  if (diffMinutes < 1440) return `${Math.round(diffMinutes / 60)}h`;
  return `${Math.round(diffMinutes / 1440)}d`;
}

function Stat({ icon: Icon, label, value, delta }) {
  return (
    <section className="stat">
      <div className="stat-icon"><Icon size={18} /></div>
      <p>{label}</p>
      <strong>{value}</strong>
      <span>{delta}</span>
    </section>
  );
}

function LoginScreen({ onLogin }) {
  const [form, setForm] = useState(demoCredentials);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const session = await api.login(form);
      storeToken(session.access_token);
      onLogin(session);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="login-shell">
      <section className="login-panel">
        <div className="brand login-brand">
          <div className="brand-mark"><MessageCircle size={22} /></div>
          <div>
            <strong>SignalDesk AI</strong>
            <span>WhatsApp Automation</span>
          </div>
        </div>
        <div>
          <p className="eyebrow">Workspace seguro</p>
          <h1>Ingresar al cockpit</h1>
        </div>
        <form onSubmit={handleSubmit} className="login-form">
          <label>
            Email
            <input
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              type="email"
              autoComplete="email"
            />
          </label>
          <label>
            Password
            <input
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              type="password"
              autoComplete="current-password"
            />
          </label>
          {error ? <p className="form-error">{error}</p> : null}
          <button className="primary login-button" disabled={isLoading}>
            {isLoading ? <Loader2 size={17} className="spin" /> : <ShieldCheck size={17} />}
            Entrar
          </button>
        </form>
      </section>
    </main>
  );
}

function Conversation({ item, active, onSelect }) {
  return (
    <button className={`conversation ${active ? "active" : ""}`} onClick={() => onSelect(item.id)}>
      <div className="avatar">{item.leadName.slice(0, 1)}</div>
      <div>
        <div className="row">
          <strong>{item.leadName}</strong>
          <span>{formatRelative(item.lastMessageAt)}</span>
        </div>
        <p>{item.preview}</p>
        <div className="tags">
          {item.tags.map((tag) => <span key={tag}>{tag}</span>)}
        </div>
      </div>
    </button>
  );
}

function App() {
  const [session, setSession] = useState(null);
  const [state, setState] = useState({
    metrics: null,
    leads: [],
    conversations: [],
    workflows: [],
    integrations: [],
    botConfig: null,
  });
  const [selectedConversationId, setSelectedConversationId] = useState(null);
  const [composerText, setComposerText] = useState("");
  const [simulator, setSimulator] = useState({
    phone: "+5491122334455",
    message: "Hola, quiero saber precios",
  });
  const [workflowDraft, setWorkflowDraft] = useState({
    name: "Follow-up comercial",
    trigger: "lead.created",
  });
  const [botDraft, setBotDraft] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState(null);

  const token = session?.access_token || getStoredToken();

  useEffect(() => {
    if (!token) return;
    loadDashboard(token);
  }, [token]);

  async function loadDashboard(activeToken) {
    setIsLoading(true);
    setError("");
    try {
      const [metrics, leads, conversations, workflows, integrations, botConfig] = await Promise.all([
        api.dashboard(activeToken),
        api.leads(activeToken),
        api.conversations(activeToken),
        api.workflows(activeToken),
        api.integrations(activeToken),
        api.botConfig(activeToken),
      ]);
      setState({ metrics, leads, conversations, workflows, integrations, botConfig });
      setBotDraft({
        ...botConfig,
        handoff_keywords_text: botConfig.handoff_keywords.join(", "),
        menu_keywords_text: botConfig.menu_keywords.join(", "),
      });
      setSelectedConversationId((current) => current || conversations[0]?.id || null);
      return conversations;
    } catch (err) {
      clearToken();
      setSession(null);
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }

  const leadById = useMemo(() => {
    return Object.fromEntries(state.leads.map((lead) => [lead.id, lead]));
  }, [state.leads]);

  const conversations = useMemo(() => {
    return state.conversations.map((conversation) => {
      const lead = leadById[conversation.lead_id];
      const lastMessage = conversation.messages.at(-1);
      return {
        ...conversation,
        leadName: lead?.name || "Lead sin nombre",
        phone: lead?.phone || "WhatsApp",
        tags: lead?.tags?.length ? lead.tags : [conversation.status],
        score: lead?.score || 50,
        preview: lastMessage?.content || "Sin mensajes todavia",
        lastMessageAt: conversation.last_message_at || lastMessage?.created_at,
      };
    });
  }, [state.conversations, leadById]);

  const active = conversations.find((conversation) => conversation.id === selectedConversationId) || conversations[0];
  const metrics = buildMetrics(state.metrics);

  function logout() {
    clearToken();
    setSession(null);
    setState({ metrics: null, leads: [], conversations: [], workflows: [], integrations: [], botConfig: null });
  }

  async function handleSimulateInbound(event) {
    event.preventDefault();
    setError("");
    setIsSending(true);
    try {
      await api.simulateWhatsApp(token, simulator);
      const refreshedConversations = await loadDashboard(token);
      setSelectedConversationId(refreshedConversations?.[0]?.id || null);
      setToast({ type: "success", message: "Mensaje inbound simulado y conversacion actualizada." });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  async function handleSendAgentMessage(event) {
    event.preventDefault();
    if (!active || !composerText.trim()) return;
    setError("");
    setIsSending(true);
    try {
      await api.sendConversationMessage(token, {
        conversation_id: active.id,
        recipient_phone: active.phone,
        content: composerText.trim(),
      });
      setComposerText("");
      await loadDashboard(token);
      setToast({ type: "success", message: "Respuesta enviada y guardada en el historial." });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  async function handleCreateWorkflow(event) {
    event.preventDefault();
    setError("");
    setIsSending(true);
    try {
      await api.createWorkflow(token, {
        name: workflowDraft.name,
        trigger: workflowDraft.trigger,
        conditions: {},
        actions: [{ type: "notify_team", team: "sales" }],
        is_active: true,
      });
      await loadDashboard(token);
      setToast({ type: "success", message: "Workflow creado y sincronizado." });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  async function handleInteractiveSelect(option) {
    if (!active) return;
    setError("");
    setIsSending(true);
    try {
      await api.sendInteractiveReply(token, {
        conversation_id: active.id,
        option_id: option.id,
        option_title: option.title,
      });
      await loadDashboard(token);
      setToast({ type: "success", message: `Opcion seleccionada: ${option.title}` });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  async function handleSaveBotConfig(event) {
    event.preventDefault();
    if (!botDraft) return;
    setError("");
    setIsSending(true);
    try {
      await api.updateBotConfig(token, {
        welcome_message: botDraft.welcome_message,
        fallback_message: botDraft.fallback_message,
        menu_title: botDraft.menu_title,
        menu_button_label: botDraft.menu_button_label,
        handoff_keywords: botDraft.handoff_keywords_text.split(",").map((item) => item.trim()).filter(Boolean),
        menu_keywords: botDraft.menu_keywords_text.split(",").map((item) => item.trim()).filter(Boolean),
        menu_sections: botDraft.menu_sections,
        option_replies: botDraft.option_replies,
      });
      await loadDashboard(token);
      setToast({ type: "success", message: "Bot settings guardados." });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  async function handleResetDemo() {
    setError("");
    setIsSending(true);
    try {
      await api.resetDemo(token);
      const refreshedConversations = await loadDashboard(token);
      setSelectedConversationId(refreshedConversations?.[0]?.id || null);
      setToast({ type: "success", message: "Demo reseteada con datos limpios." });
    } catch (err) {
      setError(err.message);
      setToast({ type: "error", message: err.message });
    } finally {
      setIsSending(false);
    }
  }

  if (!token) {
    return <LoginScreen onLogin={setSession} />;
  }

  return (
    <main className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><MessageCircle size={22} /></div>
          <div>
            <strong>SignalDesk AI</strong>
            <span>WhatsApp Automation</span>
          </div>
        </div>

        <nav>
          {[
            [Gauge, "Command Center"],
            [Inbox, "Inbox"],
            [ContactRound, "Leads"],
            [Workflow, "Workflows"],
            [BarChart3, "Analytics"],
            [PlugZap, "Integrations"],
            [ShieldCheck, "Permissions"],
          ].map(([Icon, label], index) => (
            <button className={index === 0 ? "selected" : ""} key={label} title={label}>
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </nav>

        <section className="tenant-card">
          <span>Workspace</span>
          <strong>Nova Growth Studio</strong>
          <p>Plan Growth - API connected</p>
        </section>
      </aside>

      <section className="workspace">
        {toast ? (
          <div className={`toast ${toast.type}`}>
            <span>{toast.message}</span>
            <button onClick={() => setToast(null)} title="Close"><X size={15} /></button>
          </div>
        ) : null}

        <header className="topbar">
          <div>
            <p>Operacion en vivo</p>
            <h1>Customer automation cockpit</h1>
          </div>
          <div className="actions">
            <button title="Refresh data" onClick={() => loadDashboard(token)}>
              {isLoading ? <Loader2 size={17} className="spin" /> : <Activity size={17} />}
              Sync
            </button>
            <button title="Reset demo data" onClick={handleResetDemo}>
              {isSending ? <Loader2 size={17} className="spin" /> : <Sparkles size={17} />}
              Reset demo
            </button>
            <button className="primary" title="Logout" onClick={logout}><LogOut size={17} /> Salir</button>
          </div>
        </header>

        {error ? <div className="app-alert">{error}</div> : null}

        <section className="metrics-grid">
          {metrics.map((metric) => <Stat key={metric.label} {...metric} />)}
        </section>

        <section className="main-grid">
          <div className="panel inbox-panel">
            <div className="panel-header">
              <div>
                <p>Inbox multiagente</p>
                <h2>Conversaciones prioritarias</h2>
              </div>
              <span className="live"><Activity size={14} /> Live</span>
            </div>
            <div className="conversation-list">
              {conversations.length ? (
                conversations.map((item) => (
                  <Conversation
                    item={item}
                    active={active?.id === item.id}
                    onSelect={setSelectedConversationId}
                    key={item.id}
                  />
                ))
              ) : (
                <p className="empty-state">No hay conversaciones todavia.</p>
              )}
            </div>
          </div>

          <div className="panel thread-panel">
            <div className="panel-header">
              <div>
                <p>WhatsApp - {active?.phone || "sin lead"}</p>
                <h2>{active?.leadName || "Inbox"}</h2>
              </div>
              <span className={`status ${active?.bot_enabled ? "bot-online" : "handoff"}`}>
                <Bot size={14} /> {active?.bot_enabled ? "Bot activo" : "Handoff"}
              </span>
            </div>
            <div className="thread">
              {active?.messages?.length ? (
                active.messages.map((message) => (
                  <div className={`bubble ${message.sender_type === "lead" ? "lead" : "bot"}`} key={message.id}>
                    <span>{message.sender_type === "lead" ? active.leadName : "SignalDesk AI"}</span>
                    <p>{message.content}</p>
                    <InteractivePreview
                      interactive={message.meta?.interactive}
                      onSelect={handleInteractiveSelect}
                      disabled={isSending}
                    />
                    <small className={`message-status ${message.status}`}>{message.status}</small>
                  </div>
                ))
              ) : (
                <p className="empty-state">Selecciona una conversacion para ver el historial.</p>
              )}
            </div>
            <form className="composer" onSubmit={handleSendAgentMessage}>
              <input
                placeholder="Responder con contexto comercial..."
                value={composerText}
                onChange={(event) => setComposerText(event.target.value)}
                disabled={!active || isSending}
              />
              <button title="Send" disabled={!active || isSending || !composerText.trim()}>
                {isSending ? <Loader2 size={18} className="spin" /> : <Send size={18} />}
              </button>
            </form>
          </div>

          <div className="panel intelligence-panel">
            <div className="panel-header">
              <div>
                <p>AI routing</p>
                <h2>Decision engine</h2>
              </div>
              <BrainCircuit size={22} />
            </div>
            <div className="score-ring" style={{ "--score": `${active?.score || 50}%` }}>
              <strong>{active?.score || 50}%</strong>
              <span>probabilidad de cierre</span>
            </div>
            <div className="insight-list">
              <p><Sparkles size={15} /> Intent: {active?.messages?.at(-1)?.meta?.intent || "lead qualification"}</p>
              <p><Tags size={15} /> Segment: {active?.tags?.join(", ") || "general"}</p>
              <p><Clock3 size={15} /> SLA: {state.metrics?.avg_response_seconds || 0}s first response</p>
            </div>
          </div>
        </section>

        <section className="lower-grid">
          <div className="panel simulator-panel">
            <div className="panel-header">
              <div>
                <p>WhatsApp simulator</p>
                <h2>Mensaje entrante</h2>
              </div>
              <MessageCircle size={20} />
            </div>
            <form className="simulator-form" onSubmit={handleSimulateInbound}>
              <div className="preset-row">
                {simulationPresets.map((preset) => (
                  <button
                    type="button"
                    key={preset.label}
                    onClick={() => setSimulator({ phone: preset.phone, message: preset.message })}
                  >
                    {preset.label}
                  </button>
                ))}
              </div>
              <label>
                Phone
                <input
                  value={simulator.phone}
                  onChange={(event) => setSimulator({ ...simulator, phone: event.target.value })}
                  placeholder="+5491122334455"
                />
              </label>
              <label>
                Message
                <textarea
                  value={simulator.message}
                  onChange={(event) => setSimulator({ ...simulator, message: event.target.value })}
                  placeholder="Hola, quiero saber precios"
                />
              </label>
              <button className="primary" disabled={isSending || !simulator.phone || !simulator.message}>
                {isSending ? <Loader2 size={17} className="spin" /> : <Send size={17} />}
                Simular inbound
              </button>
            </form>
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <p>Automation</p>
                <h2>Workflows activos</h2>
              </div>
            </div>
            <div className="workflow-list">
              {state.workflows.map((workflow) => (
                <article key={workflow.id}>
                  <CheckCircle2 size={18} />
                  <div>
                    <strong>{workflow.name}</strong>
                    <p>{workflow.trigger}</p>
                  </div>
                  <span>{workflow.actions.length} actions</span>
                </article>
              ))}
            </div>
            <form className="workflow-create" onSubmit={handleCreateWorkflow}>
              <input
                value={workflowDraft.name}
                onChange={(event) => setWorkflowDraft({ ...workflowDraft, name: event.target.value })}
                placeholder="Nombre del workflow"
              />
              <select
                value={workflowDraft.trigger}
                onChange={(event) => setWorkflowDraft({ ...workflowDraft, trigger: event.target.value })}
              >
                <option value="lead.created">lead.created</option>
                <option value="message.received">message.received</option>
                <option value="handoff.detected">handoff.detected</option>
              </select>
              <button className="primary" disabled={isSending || !workflowDraft.name}>
                <Workflow size={16} /> Crear
              </button>
            </form>
          </div>

          <div className="panel">
            <div className="panel-header">
              <div>
                <p>Integrations</p>
                <h2>Data sync status</h2>
              </div>
            </div>
            <div className="integration-grid">
              {state.integrations.map((integration) => (
                <article key={integration.provider}>
                  <PlugZap size={18} />
                  <strong>{integration.provider.replaceAll("_", " ")}</strong>
                  <span>{integration.status}</span>
                </article>
              ))}
            </div>
          </div>

          <div className="panel timeline-panel">
            <div className="panel-header">
              <div>
                <p>Revenue analytics</p>
                <h2>${formatNumber(state.metrics?.revenue_pipeline)} pipeline</h2>
              </div>
            </div>
            <div className="bars">
              {timeline.map((item) => <span key={item.day} style={{ height: `${item.value}%` }} title={item.day} />)}
            </div>
          </div>
        </section>

        <section className="settings-grid">
          <div className="panel bot-settings-panel">
            <div className="panel-header">
              <div>
                <p>Bot Builder</p>
                <h2>Configuracion editable</h2>
              </div>
              <Bot size={20} />
            </div>
            {botDraft ? (
              <form className="bot-settings-form" onSubmit={handleSaveBotConfig}>
                <label>
                  Mensaje de bienvenida
                  <textarea
                    value={botDraft.welcome_message}
                    onChange={(event) => setBotDraft({ ...botDraft, welcome_message: event.target.value })}
                  />
                </label>
                <label>
                  Respuesta fallback
                  <textarea
                    value={botDraft.fallback_message}
                    onChange={(event) => setBotDraft({ ...botDraft, fallback_message: event.target.value })}
                  />
                </label>
                <label>
                  Keywords para mostrar menu
                  <input
                    value={botDraft.menu_keywords_text}
                    onChange={(event) => setBotDraft({ ...botDraft, menu_keywords_text: event.target.value })}
                  />
                </label>
                <label>
                  Keywords para handoff
                  <input
                    value={botDraft.handoff_keywords_text}
                    onChange={(event) => setBotDraft({ ...botDraft, handoff_keywords_text: event.target.value })}
                  />
                </label>
                <div className="bot-option-preview">
                  {botDraft.menu_sections.flatMap((section) => section.rows).map((row) => (
                    <span key={row.id}>{row.title}</span>
                  ))}
                </div>
                <button className="primary" disabled={isSending}>
                  {isSending ? <Loader2 size={16} className="spin" /> : <CheckCircle2 size={16} />}
                  Guardar bot
                </button>
              </form>
            ) : (
              <p className="empty-state">Cargando configuracion del bot.</p>
            )}
          </div>
        </section>
      </section>
    </main>
  );
}

function InteractivePreview({ interactive, onSelect, disabled }) {
  if (!interactive) return null;

  if (interactive.type === "buttons") {
    return (
      <div className="interactive-buttons">
        {interactive.buttons.map((button) => (
          <button key={button.id} type="button" onClick={() => onSelect(button)} disabled={disabled}>
            {button.title}
          </button>
        ))}
      </div>
    );
  }

  if (interactive.type === "list") {
    return (
      <div className="interactive-list">
        <div className="interactive-list-title">{interactive.title}</div>
        {interactive.sections.map((section) => (
          <div key={section.title}>
            <strong>{section.title}</strong>
            {section.rows.map((row) => (
              <button key={row.id} type="button" onClick={() => onSelect(row)} disabled={disabled}>
                <span>{row.title}</span>
                <small>{row.description}</small>
              </button>
            ))}
          </div>
        ))}
      </div>
    );
  }

  return null;
}

function buildMetrics(metrics) {
  return [
    { icon: MessageCircle, label: "Mensajes hoy", value: formatNumber(metrics?.messages_today), delta: "API live" },
    { icon: ContactRound, label: "Leads totales", value: formatNumber(metrics?.total_leads), delta: `${metrics?.conversion_rate || 0}% conversion` },
    { icon: Bot, label: "Resolucion IA", value: `${metrics?.ai_resolution_rate || 0}%`, delta: metrics?.bot_health || "loading" },
    { icon: Clock3, label: "First response", value: `${metrics?.avg_response_seconds || 0}s`, delta: `${metrics?.active_conversations || 0} active` },
  ];
}

createRoot(document.getElementById("root")).render(<App />);
