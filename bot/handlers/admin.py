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
@router.message(Command("warroom"))
async def cmd_warroom(message: Message):
    if not is_admin(message.from_user.id):
        return
    stats = await db.get_stats()
    up = int(metrics.uptime())
    await message.answer(
        f"☠️ <b>DEVIL WAR ROOM</b>\n\n"
        f"Uptime: {up // 3600}h {(up % 3600) // 60}m\n"
        f"Users: {stats['users']}\n"
        f"Accounts in arsenal: {stats['accounts']}\n"
        f"Active swarms: {stats['monitors']}\n"
        f"Total hits: {stats['hits']}\n"
        f"Claimed: {stats['claimed']}\n"
        f"Scans: {metrics.scans}\n"
        f"Success rate: {metrics.success_rate}%\n\n"
        f"Aggression: {settings.aggression_level}/10",
        parse_mode="HTML"
    )

@router.message(Command("arsenal"))
async def cmd_arsenal(message: Message):
    if not is_admin(message.from_user.id):
        return
    accounts = await db.get_healthy_accounts(50)
    if not accounts:
        await message.answer("Arsenal empty. Add accounts.")
        return
    text = "<b>🔫 Account Arsenal</b>\n\n"
    for a in accounts[:20]:
        text += f"#{a['id']} {a['email'][:20]}... | HP {a['health']} | ✓{a['success_count']} ✗{a['fail_count']}\n"
    await message.answer(text, parse_mode="HTML")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    if not is_admin(message.from_user.id):
        return
    await cmd_warroom(message)
