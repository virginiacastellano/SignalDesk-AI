import { Bot, Clock3, ContactRound, MessageCircle } from "lucide-react";

export const metrics = [
  { icon: MessageCircle, label: "Mensajes hoy", value: "2,847", delta: "+18.4%" },
  { icon: ContactRound, label: "Leads nuevos", value: "184", delta: "+11.2%" },
  { icon: Bot, label: "Resolucion IA", value: "74%", delta: "+6.8%" },
  { icon: Clock3, label: "First response", value: "42s", delta: "-31%" },
];

export const conversations = [
  {
    name: "Valentina Rios",
    phone: "+54 9 11 3842 9910",
    time: "2m",
    preview: "Quiero saber si el plan incluye integracion con mi CRM.",
    tags: ["enterprise", "hot lead"],
    messages: [
      { from: "lead", text: "Hola, quiero automatizar WhatsApp para mi equipo comercial." },
      { from: "bot", text: "Perfecto, Valentina. Puedo ayudarte a evaluar volumen, CRM y tipo de atencion. Cuantos mensajes reciben por dia?" },
      { from: "lead", text: "Entre 400 y 600. Quiero saber si el plan incluye integracion con mi CRM." },
      { from: "bot", text: "Si. Para ese volumen recomendamos Growth con CRM webhook, etiquetas automaticas y handoff a vendedores. Te preparo una demo breve?" },
    ],
  },
  { name: "Mateo Alvarez", time: "8m", preview: "Necesito recuperar carritos abandonados.", tags: ["ecommerce", "workflow"], messages: [], phone: "+54 9 11 4455 1200" },
  { name: "Sofia Mendes", time: "14m", preview: "Puede hablar en portugues?", tags: ["support", "pt-BR"], messages: [], phone: "+55 11 99110 7700" },
  { name: "Lucas Torres", time: "23m", preview: "Quiero comparar con Zendesk.", tags: ["comparison"], messages: [], phone: "+54 9 351 612 8834" },
];

export const workflows = [
  { name: "Lead qualification", description: "Etiqueta leads por intencion, presupuesto y urgencia.", runs: 942 },
  { name: "Human handoff", description: "Deriva conversaciones con reclamos o alta oportunidad.", runs: 318 },
  { name: "Abandoned cart rescue", description: "Follow-up por WhatsApp con template aprobado.", runs: 521 },
];

export const integrations = [
  { name: "Google Sheets", status: "synced" },
  { name: "Gmail", status: "ready" },
  { name: "HubSpot mock", status: "connected" },
  { name: "Webhook CRM", status: "active" },
];

export const timeline = [
  { day: "Mon", value: 42 },
  { day: "Tue", value: 56 },
  { day: "Wed", value: 48 },
  { day: "Thu", value: 74 },
  { day: "Fri", value: 66 },
  { day: "Sat", value: 38 },
  { day: "Sun", value: 51 },
];
