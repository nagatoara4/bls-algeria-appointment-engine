from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from bot.keyboards import main_menu
from bot.services.storage import register_user
from bot.states import BookingStates

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    register_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "🇩🇿 <b>BLS Algeria Appointment Engine</b>\n\n"
        "I help you monitor and manage appointment slots.\n"
        "Press the button below to begin.",
        reply_markup=main_menu(),
        parse_mode="HTML"
    )

@router.message(Command("cancel"))
@router.message(F.text == "❌ Cancel")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Flow cancelled.", reply_markup=main_menu())

@router.message(F.text == "📊 Status")
async def cmd_status(message: Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        await message.answer("No active session.")
        return
    text = "<b>Current session</b>\n"
    for k, v in data.items():
        text += f"• {k}: {v}\n"
    await message.answer(text, parse_mode="HTML")
