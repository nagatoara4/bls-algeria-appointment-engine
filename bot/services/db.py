import aiosqlite
from pathlib import Path
from bot.config import settings
from typing import List, Dict, Any, Optional
import time

DB_PATH = Path(settings.db_path)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    first_seen REAL,
    last_seen REAL,
    bookings INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE,
    password TEXT,
    cookies TEXT,
    health INTEGER DEFAULT 100,
    last_used REAL,
    success_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0,
    active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS monitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    city TEXT,
    visa_type TEXT,
    category TEXT,
    aggression INTEGER DEFAULT 5,
    active INTEGER DEFAULT 1,
    created REAL,
    last_hit REAL,
    hits INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS hits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    city TEXT,
    visa_type TEXT,
    category TEXT,
    slot_date TEXT,
    slot_time TEXT,
    claimed INTEGER DEFAULT 0,
    account_id INTEGER
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts REAL,
    kind TEXT,
    user_id INTEGER,
    detail TEXT
);
"""

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()

async def upsert_user(user_id: int, username: Optional[str] = None):
    now = time.time()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO users (id, username, first_seen, last_seen, bookings)
               VALUES (?, ?, ?, ?, 0)
               ON CONFLICT(id) DO UPDATE SET username=excluded.username, last_seen=excluded.last_seen""",
            (user_id, username, now, now)
        )
        await db.commit()

async def add_account(email: str, password: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT OR IGNORE INTO accounts (email, password, last_used) VALUES (?, ?, ?)",
            (email, password, time.time())
        )
        await db.commit()
        return cur.lastrowid

async def get_healthy_accounts(limit: int = 20) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM accounts WHERE active = 1 AND health > 30 ORDER BY health DESC, last_used ASC LIMIT ?",
            (limit,)
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def update_account_health(account_id: int, delta: int, success: bool = False):
    async with aiosqlite.connect(DB_PATH) as db:
        if success:
            await db.execute(
                "UPDATE accounts SET health = MIN(100, health + ?), success_count = success_count + 1, last_used = ? WHERE id = ?",
                (delta, time.time(), account_id)
            )
        else:
            await db.execute(
                "UPDATE accounts SET health = MAX(0, health + ?), fail_count = fail_count + 1, last_used = ? WHERE id = ?",
                (delta, time.time(), account_id)
            )
        await db.commit()

async def add_monitor(user_id: int, city: str, visa_type: str, category: str, aggression: int = 8) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO monitors (user_id, city, visa_type, category, aggression, active, created) VALUES (?, ?, ?, ?, ?, 1, ?)",
            (user_id, city, visa_type, category, aggression, time.time())
        )
        await db.commit()
        return cur.lastrowid

async def get_active_monitors(user_id: int = None) -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        if user_id:
            cur = await db.execute("SELECT * FROM monitors WHERE user_id = ? AND active = 1", (user_id,))
        else:
            cur = await db.execute("SELECT * FROM monitors WHERE active = 1")
        return [dict(r) for r in await cur.fetchall()]

async def stop_all_monitors(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE monitors SET active = 0 WHERE user_id = ?", (user_id,))
        await db.commit()

async def log_hit(city: str, visa_type: str, category: str, slot_date: str, slot_time: str, account_id: int = None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO hits (ts, city, visa_type, category, slot_date, slot_time, account_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (time.time(), city, visa_type, category, slot_date, slot_time, account_id)
        )
        await db.commit()

async def get_stats() -> Dict[str, Any]:
    async with aiosqlite.connect(DB_PATH) as db:
        users = (await (await db.execute("SELECT COUNT(*) FROM users")).fetchone())[0]
        accounts = (await (await db.execute("SELECT COUNT(*) FROM accounts WHERE active = 1")).fetchone())[0]
        monitors = (await (await db.execute("SELECT COUNT(*) FROM monitors WHERE active = 1")).fetchone())[0]
        hits = (await (await db.execute("SELECT COUNT(*) FROM hits")).fetchone())[0]
        claimed = (await (await db.execute("SELECT COUNT(*) FROM hits WHERE claimed = 1")).fetchone())[0]
        return {"users": users, "accounts": accounts, "monitors": monitors, "hits": hits, "claimed": claimed}

async def log_event(kind: str, user_id: int = None, detail: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO events (ts, kind, user_id, detail) VALUES (?, ?, ?, ?)",
            (time.time(), kind, user_id, detail)
        )
        await db.commit()
