from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards import cities_kb, visa_types_kb, categories_kb
from bot.states import BookingStates
from bot.services import monitor as mon, db
from bot.config import settings

router = Router()

@router.message(Command("monitor"))
@router.message(Command("swarm"))
@router.message(F.text == "📡 Monitor")
async def cmd_swarm(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_city)
    await state.update_data(mode="swarm")
    await message.answer(
        f"🔥 <b>DEVIL SWARM</b>\nAggression level: {settings.aggression_level}/10\n\nSelect center:",
        reply_markup=cities_kb(),
        parse_mode="HTML"
    )

@router.message(Command("stopmonitor"))
@router.message(Command("stopall"))
async def cmd_stop(message: Message):
    await mon.stop_user_swarms(message.from_user.id)
    await message.answer("🛑 All swarms killed.")

@router.message(Command("status"))
async def cmd_status(message: Message):
    active = await db.get_active_monitors(message.from_user.id)
    if not active:
        await message.answer("No active swarms.")
        return
    text = "<b>🔥 Active DEVIL Swarms</b>\n\n"
    for m in active:
        text += f"#{m['id']} — {m['city']} | {m['visa_type']} | {m['category']} | agg={m.get('aggression', 8)}\n"
    await message.answer(text, parse_mode="HTML")
