from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_menu
from bot.services import db
from bot.config import settings

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.upsert_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"☠️ <b>BLS DEVIL ENGINE v3.0</b>\n\n"
        f"Aggression: {settings.aggression_level}/10\n"
        f"Scan interval: {settings.scan_interval_sec}s\n\n"
        f"/swarm — launch high-frequency scanner\n"
        f"/book — manual booking flow\n"
        f"/status — active swarms\n"
        f"/stopall — kill everything\n"
        f"/warroom — live metrics (admin)",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@router.message(Command("cancel"))
@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu())
