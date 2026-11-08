# BLS Algeria Appointment Engine v2.0

**High-performance, production-grade appointment monitoring and booking automation system.**

Completely rewritten and upgraded for maximum reliability, concurrency, observability and extensibility.

> Educational / research / personal automation tool.  
> Respect the target service terms of use.

## Architecture Highlights (v2)

- **Async-first** (aiogram 3 + asyncio)
- **Persistent storage** (SQLite via aiosqlite)
- **Concurrent slot monitors** per user/city/visa combination
- **Rate-limited outbound actions**
- **Structured logging + metrics**
- **Health endpoint + graceful shutdown**
- **Multi-profile support** (multiple applicants)
- **Admin analytics dashboard**
- **Docker-ready**
- **Full type hints + pydantic validation**
- **Unit tests for core services**

## Project Layout

```
bls-algeria-appointment-engine/
├── bot/
│   ├── main.py
│   ├── config.py
│   ├── states.py
│   ├── keyboards.py
│   ├── middlewares/
│   │   └── throttling.py
│   ├── handlers/
│   │   ├── start.py
│   │   ├── booking.py
│   │   ├── monitor.py
│   │   ├── admin.py
│   │   └── common.py
│   └── services/
│       ├── db.py
│       ├── slots.py
│       ├── monitor.py
│       ├── session.py
│       └── metrics.py
├── scripts/
│   ├── individual_appointment.user.js
│   └── payment_receipt.user.js
├── tests/
│   └── test_slots.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Quick Start

```bash
git clone https://github.com/nagatoara4/bls-algeria-appointment-engine.git
cd bls-algeria-appointment-engine
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit BOT_TOKEN and ADMIN_IDS
python -m bot.main
```

Docker:

```bash
docker compose up -d --build
```

## Key Commands

| Command | Description |
|---------|-------------|
| `/start` | Launch |
| `/book` | Start booking flow |
| `/monitor` | Start continuous slot monitoring |
| `/stopmonitor` | Stop monitors |
| `/profiles` | Manage applicant profiles |
| `/status` | Session + monitor status |
| `/admin` | Admin panel |
| `/stats` | System metrics |
| `/broadcast` | Admin broadcast |

## What Changed from v1 → v2

- SQLite persistence instead of plain JSON
- Real concurrent monitoring loops with cancellation
- Middleware rate limiting
- Metrics collection (scans, hits, users, uptime)
- Health checks
- Docker support
- Better separation of concerns
- Tests for slot engine
- Cleaner error handling and recovery

## License

MIT

Upgraded by ylivo4real 👾
