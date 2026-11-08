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

CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    label TEXT,
    first_name TEXT,
    last_name TEXT,
    birth TEXT,
    passport TEXT,
    issue_date TEXT,
    expiry_date TEXT,
    issue_place TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS monitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    city TEXT,
    visa_type TEXT,
    category TEXT,
    active INTEGER DEFAULT 1,
    created REAL,
    last_hit REAL,
    FOREIGN KEY(user_id) REFERENCES users(id)
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

async def increment_booking(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET bookings = bookings + 1 WHERE id = ?", (user_id,))
        await db.commit()

async def get_user_count() -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        row = await cur.fetchone()
        return row[0] if row else 0

async def get_all_users() -> List[Dict[str, Any]]:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute("SELECT * FROM users ORDER BY last_seen DESC")
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def add_monitor(user_id: int, city: str, visa_type: str, category: str) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO monitors (user_id, city, visa_type, category, active, created) VALUES (?, ?, ?, ?, 1, ?)",
            (user_id, city, visa_type, category, time.time())
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
        rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def stop_monitor(monitor_id: int, user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE monitors SET active = 0 WHERE id = ? AND user_id = ?", (monitor_id, user_id))
        await db.commit()

async def stop_all_monitors(user_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE monitors SET active = 0 WHERE user_id = ?", (user_id,))
        await db.commit()

async def log_event(kind: str, user_id: int = None, detail: str = ""):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO events (ts, kind, user_id, detail) VALUES (?, ?, ?, ?)",
            (time.time(), kind, user_id, detail)
        )
        await db.commit()
