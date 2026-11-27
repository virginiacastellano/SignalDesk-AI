# SignalDesk AI

SignalDesk AI is a portfolio-grade SaaS platform for WhatsApp customer automation with AI, lead management, workflows, analytics and multi-tenant operations.

It is intentionally built like a commercial startup product: FastAPI backend, React dashboard, PostgreSQL, Redis, Celery workers, Docker Compose, mocked external integrations for local demos, and clear extension points for real WhatsApp Cloud API and OpenAI credentials.

## Product Capabilities

- WhatsApp Cloud API adapter for inbound webhooks, outbound text messages and templates.
- AI assistant service using OpenAI Responses API with recent conversation context.
- Configurable bot builder for welcome copy, fallback replies, menu keywords and handoff keywords.
- Interactive WhatsApp-style menus with clickable options in the local dashboard demo.
- Demo reset endpoint to restore clean tenant data before a portfolio walkthrough.
- Multi-tenant data model with tenants, users, memberships, roles and tenant-scoped resources.
- JWT authentication with role-ready authorization boundaries.
- Lead CRM, conversation history, tags, bot handoff state and message delivery status.
- Workflow engine foundation for rules, follow-ups, tagging and team assignment.
- Celery background tasks for follow-ups and integration sync jobs.
- SaaS dashboard UI with inbox, lead intelligence, bot status, workflow status and analytics.
- Mock Google Sheets, Gmail and CRM integrations for local demos.
- Dockerized infrastructure with PostgreSQL, Redis, FastAPI, Celery, React and Nginx.

## Tech Stack

Backend: Python, FastAPI, SQLAlchemy 2, PostgreSQL, Redis, Celery, Pydantic, JWT.

Frontend: React, Vite, lucide-react, responsive CSS inspired by modern SaaS dashboards.

Infrastructure: Docker Compose, Nginx reverse proxy, environment-driven configuration.

AI: OpenAI Python SDK through the Responses API.

## Repository Layout

```text
whatsapp-ai-saas/
  backend/
    app/
      api/                  FastAPI routers and dependencies
      core/                 config, logging, security, error handling
      domain/               database models and request/response schemas
      infrastructure/       database, repositories, provider adapters
      services/             application use cases
      workers/              Celery app and tasks
      seeds/                demo seed data
    tests/
  frontend/
    src/
      data/                 demo dashboard data
      main.jsx              SaaS product UI
      styles.css            responsive design system
  infra/nginx/
  docs/
```

## Quick Start

1. Copy backend environment variables:

```bash
cp backend/.env.example backend/.env
```

2. Start the full stack:

```bash
docker compose up --build
```

3. Seed demo data:

```bash
docker compose exec backend python -m app.seeds.seed_demo
```

4. Open the product:

- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs
- Nginx gateway: http://localhost:8080

Demo credentials after seeding:

```text
founder@novagrowth.io
Password123!
```

## V1 Demo Flow

For a clean portfolio demo:

1. Login at `http://localhost:5173`.
2. Click `Reset demo`.
3. Use the `Menu` preset in the WhatsApp simulator.
4. Click `Planes y precios` inside the interactive menu.
5. Use the composer to send a manual agent response.
6. Edit the welcome message in `Bot Builder`, save, and simulate `Menu` again.

See [docs/DEMO_FLOW.md](docs/DEMO_FLOW.md) for the short video script.

## API Highlights

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/bot-config`
- `PUT /api/v1/bot-config`
- `POST /api/v1/demo/reset`
- `GET /api/v1/conversations`
- `POST /api/v1/conversations/messages`
- `GET /api/v1/leads`
- `POST /api/v1/workflows`
- `GET /api/v1/analytics/dashboard`
- `GET /api/v1/whatsapp/webhook`
- `POST /api/v1/whatsapp/webhook`
- `POST /api/v1/whatsapp/simulate`
- `POST /api/v1/whatsapp/interactive-reply`
- `POST /api/v1/whatsapp/messages/text`
- `POST /api/v1/integrations/google-sheets/sync`

## WhatsApp Setup

Set these variables in `backend/.env` when using real WhatsApp Cloud API credentials:

```env
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_BUSINESS_ACCOUNT_ID=
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_VERIFY_TOKEN=
PUBLIC_WEBHOOK_URL=
```

Configure the Meta webhook URL as:

```text
https://your-domain.com/api/v1/whatsapp/webhook
```

For portfolio demos, missing WhatsApp credentials automatically trigger mocked sends.

## OpenAI Setup

Set:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5
```

The AI provider calls `client.responses.create(...)` and normalizes the output into:

- `reply`
- `intent`
- `handoff_required`

This keeps the business logic decoupled from a single AI vendor or model family.

## Deployment Notes

For production, deploy the backend and worker as separate services. Use managed PostgreSQL and Redis, store secrets in a cloud secret manager, terminate TLS at the load balancer or Nginx, and run Alembic migrations during release. The V1 portfolio build auto-creates tables in development to keep the demo easy to run.

Recommended hardening:

- Add Alembic migration files and migration CI checks.
- Add row-level security in PostgreSQL for tenant isolation.
- Persist WhatsApp webhook idempotency keys.
- Add OpenTelemetry tracing and structured request IDs.
- Split teams, permissions and audit logs into dedicated modules.
- Add billing/subscription entities for Stripe or Mercado Pago.

## Portfolio Story

This project is designed to demonstrate senior backend judgment:

- clear module boundaries,
- tenant-scoped data access,
- provider adapters for external APIs,
- async FastAPI implementation,
- background task architecture,
- realistic SaaS dashboard,
- production-oriented Docker setup,
- and an upgrade path from demo mocks to real integrations.

## Workana Description

SignalDesk AI is a multi-tenant SaaS demo for WhatsApp customer automation. It includes a FastAPI backend, JWT authentication, PostgreSQL data model, Redis/Celery jobs, a React dashboard, WhatsApp webhook simulation, interactive bot menus, handoff to human agents, workflow creation, analytics and a configurable bot builder. It is designed as a production-style foundation for businesses that want to automate customer conversations and lead qualification over WhatsApp.
