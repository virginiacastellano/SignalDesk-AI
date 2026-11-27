# Demo Flow

Use this flow for a 60-90 second Workana or recruiter demo.

## 1. Login

Open `http://localhost:5173` and login with:

```text
founder@novagrowth.io
Password123!
```

## 2. Show The Cockpit

Point out:

- live metrics from FastAPI/PostgreSQL;
- WhatsApp inbox;
- conversation detail;
- AI routing panel;
- workflows and integrations.

## 3. Simulate WhatsApp

Use the WhatsApp simulator presets:

- `Menu`: shows an interactive list.
- `Precios`: shows automated commercial reply.
- `Handoff`: disables bot and marks the conversation for a human.

## 4. Click Menu Options

Click `Planes y precios` in the interactive menu. The platform stores the selected option as an inbound message and creates a bot reply.

## 5. Human Response

Use the composer to send a manual message. The message is saved as `sent`.

## 6. Bot Builder

Edit the welcome message or keywords in `Bot Builder`, save, then simulate `Menu` again to show that the bot is configurable.

## 7. Reset

Use `Reset demo` to return to clean demo data.
