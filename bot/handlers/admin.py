from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import settings
from bot.services.storage import get_all_users, get_user_count

router = Router()

def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_id_list

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        return
    count = get_user_count()
    await message.answer(
        f"🔧 <b>Admin Panel</b>\n\n"
        f"Users registered: {count}\n"
        f"Commands:\n"
        f"/users — export user list\n"
        f"/broadcast <text> — send to all",
        parse_mode="HTML"
    )

@router.message(Command("users"))
async def cmd_users(message: Message):
    if not is_admin(message.from_user.id):
        return
    users = get_all_users()
    if not users:
        await message.answer("No users yet.")
        return
    lines = [f"{u['id']} | @{u.get('username') or '-'} | bookings={u.get('bookings', 0)}" for u in users]
    text = "ID | Username | Bookings\n" + "\n".join(lines[:100])
    await message.answer(f"<pre>{text}</pre>", parse_mode="HTML")

@router.message(Command("broadcast"))
async def cmd_broadcast(message: Message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /broadcast your message here")
        return
    text = parts[1]
    users = get_all_users()
    sent = 0
    for u in users:
        try:
            await message.bot.send_message(u["id"], text)
            sent += 1
        except Exception:
            pass
    await message.answer(f"Broadcast sent to {sent} users.")
