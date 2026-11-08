from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_menu
from bot.services import db

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await db.upsert_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "🇩🇿 <b>BLS Algeria Appointment Engine v2</b>\n\n"
        "High-performance monitoring + booking system.\n\n"
        "/book — start booking flow\n"
        "/monitor — continuous slot watch\n"
        "/status — your monitors\n"
        "/stopmonitor — stop all",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@router.message(Command("cancel"))
@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu())
