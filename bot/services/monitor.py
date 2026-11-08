"""
Concurrent monitor manager.
Each active monitor runs an independent asyncio task.
"""
import asyncio
import logging
from typing import Dict
from bot.services import db
from bot.services.slots import generate_slots
from bot.config import settings

logger = logging.getLogger(__name__)

# user_id -> list of running tasks
_tasks: Dict[int, list] = {}

async def _monitor_loop(bot, user_id: int, monitor_id: int, city: str, visa_type: str, category: str):
    logger.info("Monitor %s started for user %s (%s/%s/%s)", monitor_id, user_id, city, visa_type, category)
    try:
        while True:
            slots = generate_slots(city, visa_type, category, count=3)
            if slots:
                text = f"🔔 <b>Slots detected</b>\nCenter: {city}\nVisa: {visa_type} — {category}\n\n"
                for s in slots:
                    text += f"• {s['date']} {s['time']} (score {s['score']})\n"
                text += "\nUse /book to start a booking flow."
                try:
                    await bot.send_message(user_id, text, parse_mode="HTML")
                    await db.log_event("slot_hit", user_id, f"{city}|{visa_type}|{category}")
                except Exception as e:
                    logger.warning("Failed to notify user %s: %s", user_id, e)
            await asyncio.sleep(settings.scan_interval_sec)
    except asyncio.CancelledError:
        logger.info("Monitor %s cancelled", monitor_id)
        raise

async def start_monitor(bot, user_id: int, city: str, visa_type: str, category: str) -> int:
    active = await db.get_active_monitors(user_id)
    if len(active) >= settings.max_monitors_per_user:
        raise RuntimeError(f"Max monitors reached ({settings.max_monitors_per_user})")

    monitor_id = await db.add_monitor(user_id, city, visa_type, category)
    task = asyncio.create_task(_monitor_loop(bot, user_id, monitor_id, city, visa_type, category))
    _tasks.setdefault(user_id, []).append((monitor_id, task))
    await db.log_event("monitor_start", user_id, f"{monitor_id}|{city}")
    return monitor_id

async def stop_user_monitors(user_id: int):
    await db.stop_all_monitors(user_id)
    tasks = _tasks.pop(user_id, [])
    for mid, task in tasks:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
    await db.log_event("monitor_stop_all", user_id)

async def restore_monitors(bot):
    """Re-attach tasks after restart."""
    monitors = await db.get_active_monitors()
    for m in monitors:
        task = asyncio.create_task(
            _monitor_loop(bot, m["user_id"], m["id"], m["city"], m["visa_type"], m["category"])
        )
        _tasks.setdefault(m["user_id"], []).append((m["id"], task))
    logger.info("Restored %d active monitors", len(monitors))
