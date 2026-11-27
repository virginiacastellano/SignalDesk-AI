# Architecture

SignalDesk AI follows a pragmatic Clean Architecture layout:

- `domain`: SQLAlchemy entities and Pydantic DTOs that describe the product language.
- `services`: use cases for auth, conversations, analytics and workflows.
- `infrastructure`: database sessions, repositories and external provider adapters.
- `api`: FastAPI routing and dependency wiring.
- `workers`: Celery tasks for scheduled follow-ups and integration syncs.

## Multi-Tenant Strategy

Every business object carries `tenant_id`. API dependencies derive the active tenant from the JWT, and repository methods filter data by tenant. For a larger production deployment, the next step would be PostgreSQL row-level security plus tenant-scoped audit logs.

## AI Strategy

The AI adapter uses OpenAI's Responses API with a business prompt plus recent conversation context. The service returns a normalized result with `reply`, `intent` and `handoff_required`, so the rest of the platform is not coupled to one model provider.

## WhatsApp Strategy

The WhatsApp adapter wraps Cloud API text and template messages. Webhooks normalize inbound messages into leads, conversations and message history. Missing credentials fall back to mocked responses so the demo remains usable.

## Production Hardening Roadmap

- Alembic migrations and CI migration checks.
- Row-level security policies per tenant.
- Idempotency keys for WhatsApp webhook events.
- Dead-letter queues for Celery jobs.
- Observability with OpenTelemetry traces and dashboard alerts.
- Secrets managed by a cloud secret manager instead of `.env` files.
