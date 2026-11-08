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
async def cmd_monitor(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_city)
    await state.update_data(mode="monitor")
    await message.answer("Select center to monitor:", reply_markup=cities_kb())

@router.message(Command("stopmonitor"))
async def cmd_stop(message: Message):
    await mon.stop_user_monitors(message.from_user.id)
    await message.answer("All your monitors stopped.")

@router.message(Command("status"))
async def cmd_status(message: Message):
    active = await db.get_active_monitors(message.from_user.id)
    if not active:
        await message.answer("No active monitors.")
        return
    text = "<b>Active monitors</b>\n\n"
    for m in active:
        text += f"#{m['id']} — {m['city']} | {m['visa_type']} | {m['category']}\n"
    await message.answer(text, parse_mode="HTML")
