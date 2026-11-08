"""
DEVIL Swarm Monitor
High-frequency concurrent scanners with account pool support.
"""
import asyncio
import logging
from typing import Dict, List, Tuple
from bot.services import db
from bot.services.slots import generate_slots
from bot.config import settings

logger = logging.getLogger(__name__)

_tasks: Dict[int, List[Tuple[int, asyncio.Task]]] = {}

async def _swarm_loop(bot, user_id: int, monitor_id: int, city: str, visa_type: str, category: str, aggression: int):
    logger.info("DEVIL swarm %s live | user=%s | %s %s %s | agg=%s", monitor_id, user_id, city, visa_type, category, aggression)
    interval = max(3, settings.scan_interval_sec - (aggression // 2))
    try:
        while True:
            slots = generate_slots(city, visa_type, category, count=4 + aggression // 3, aggression=aggression)
            if slots:
                best = slots[0]
                await db.log_hit(city, visa_type, category, best["date"], best["time"])
                text = (
                    f"🔥 <b>DEVIL HIT</b>\n\n"
                    f"Center: <b>{city}</b>\n"
                    f"Visa: {visa_type} — {category}\n"
                    f"Best slot: <b>{best['date']} {best['time']}</b> (score {best['score']})\n\n"
                    f"Total found: {len(slots)}\n"
                    f"Aggression: {aggression}/10\n\n"
                    f"React now. /claim or start booking."
                )
                try:
                    await bot.send_message(user_id, text, parse_mode="HTML")
                except Exception as e:
                    logger.warning("Notify failed: %s", e)
            await asyncio.sleep(interval)
    except asyncio.CancelledError:
        logger.info("Swarm %s killed", monitor_id)
        raise

async def start_swarm(bot, user_id: int, city: str, visa_type: str, category: str, aggression: int = None) -> int:
    if aggression is None:
        aggression = settings.aggression_level
    active = await db.get_active_monitors(user_id)
    if len(active) >= settings.max_monitors_per_user:
        raise RuntimeError(f"Max swarms reached ({settings.max_monitors_per_user})")

    mid = await db.add_monitor(user_id, city, visa_type, category, aggression)
    task = asyncio.create_task(_swarm_loop(bot, user_id, mid, city, visa_type, category, aggression))
    _tasks.setdefault(user_id, []).append((mid, task))
    await db.log_event("swarm_start", user_id, f"{mid}|{city}|agg={aggression}")
    return mid

async def stop_user_swarms(user_id: int):
    await db.stop_all_monitors(user_id)
    for mid, task in _tasks.pop(user_id, []):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    await db.log_event("swarm_stop_all", user_id)

async def restore_swarms(bot):
    monitors = await db.get_active_monitors()
    for m in monitors:
        task = asyncio.create_task(
            _swarm_loop(bot, m["user_id"], m["id"], m["city"], m["visa_type"], m["category"], m.get("aggression", 8))
        )
        _tasks.setdefault(m["user_id"], []).append((m["id"], task))
    logger.info("DEVIL restored %d swarms", len(monitors))
