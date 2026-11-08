from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import settings
from bot.services import db
from bot.services.metrics import metrics

router = Router()

def is_admin(uid: int) -> bool:
    return uid in settings.admin_id_list

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    count = await db.get_user_count()
    await message.answer(
        f"🔧 <b>Admin</b>\n\nUsers: {count}\n"
        f"/stats — metrics\n/users — list\n/broadcast <text>",
        parse_mode="HTML"
    )

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        return
    up = int(metrics.uptime())
    await message.answer(
        f"📊 <b>Metrics</b>\n\n"
        f"Uptime: {up // 3600}h {(up % 3600) // 60}m\n"
        f"Scans: {metrics.scans}\n"
        f"Hits: {metrics.hits}\n"
        f"Users: {await db.get_user_count()}",
        parse_mode="HTML"
    )

@router.message(Command("users"))
async def cmd_users(message: Message):
    if not is_admin(message.from_user.id):
        return
    users = await db.get_all_users()
    if not users:
        await message.answer("No users.")
        return
    lines = [f"{u['id']} | @{u.get('username') or '-'} | {u.get('bookings', 0)}" for u in users[:80]]
    await message.answer("<pre>" + "\n".join(lines) + "</pre>", parse_mode="HTML")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /broadcast text")
        return
    text = parts[1]
    users = await db.get_all_users()
    sent = 0
    for u in users:
        try:
            await message.bot.send_message(u["id"], text)
            sent += 1
        except Exception:
            pass
    await message.answer(f"Sent to {sent} users.")
