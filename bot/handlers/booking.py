from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from bot.states import BookingStates
from bot.keyboards import (
    countries_kb, cities_kb, visa_types_kb,
    categories_kb, slots_kb, main_menu
)
from bot.services.slots import generate_slots
from bot.services import db, monitor as mon
from bot.services.metrics import metrics
from bot.config import settings

router = Router()

@router.message(Command("book"))
@router.message(F.text == "🚀 Start Booking")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_country)
    await state.update_data(mode="book")
    await message.answer("Select destination country:", reply_markup=countries_kb())

@router.callback_query(F.data.startswith("country:"))
async def on_country(callback: CallbackQuery, state: FSMContext):
    country = callback.data.split(":", 1)[1]
    await state.update_data(country=country)
    await state.set_state(BookingStates.choosing_city)
    await callback.message.edit_text(
        f"Country: <b>{country}</b>\n\nSelect center:",
        reply_markup=cities_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("city:"))
async def on_city(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.update_data(city=city)
    mode = data.get("mode", "book")

    await state.set_state(BookingStates.choosing_visa_type)
    label = "for swarm" if mode == "swarm" else ""
    await callback.message.edit_text(
        f"Center: <b>{city}</b>\n\nSelect visa type {label}:",
        reply_markup=visa_types_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("visa:"))
async def on_visa(callback: CallbackQuery, state: FSMContext):
    visa = callback.data.split(":", 1)[1]
    await state.update_data(visa_type=visa)
    await state.set_state(BookingStates.choosing_category)
    await callback.message.edit_text(
        f"Visa: <b>{visa}</b>\n\nSelect category:",
        reply_markup=categories_kb(visa),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("cat:"))
async def on_category(callback: CallbackQuery, state: FSMContext):
    category = callback.data.split(":", 1)[1]
    data = await state.get_data()
    await state.update_data(category=category)
    mode = data.get("mode", "book")
    city = data["city"]
    visa = data["visa_type"]

    if mode == "swarm":
        try:
            mid = await mon.start_swarm(
                callback.bot, callback.from_user.id, city, visa, category,
                aggression=settings.aggression_level
            )
            await callback.message.edit_text(
                f"🔥 <b>DEVIL SWARM #{mid} ONLINE</b>\n\n"
                f"{city} | {visa} | {category}\n"
                f"Aggression: {settings.aggression_level}/10\n\n"
                f"You will be notified on every hit.\n"
                f"/stopall to kill."
            )
        except RuntimeError as e:
            await callback.message.edit_text(str(e))
        await state.clear()
        await callback.answer()
        return

    # normal book
    await callback.message.edit_text("⚡ Scanning at maximum speed...")
    metrics.scans += 1
    slots = generate_slots(city, visa, category, aggression=settings.aggression_level)
    await state.update_data(slots=slots)
    await state.set_state(BookingStates.confirming_slot)

    if not slots:
        await callback.message.edit_text("No slots. Swarm recommended.")
        await callback.answer()
        return

    text = (
        f"🔥 <b>{len(slots)} slots found</b>\n"
        f"{data.get('country', '')} | {city} | {visa} | {category}\n\n"
        f"Select:"
    )
    await callback.message.edit_text(text, reply_markup=slots_kb(slots), parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data == "refresh_slots")
async def refresh_slots(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    metrics.scans += 1
    slots = generate_slots(
        data.get("city", "ALG1"),
        data.get("visa_type", "C - Short Stay"),
        data.get("category", "Tourism"),
        aggression=settings.aggression_level
    )
    await state.update_data(slots=slots)
    await callback.message.edit_text(
        f"🔄 Refreshed — {len(slots)} slots:",
        reply_markup=slots_kb(slots)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("slot:"))
async def on_slot(callback: CallbackQuery, state: FSMContext):
    slot_id = callback.data.split(":", 1)[1]
    data = await state.get_data()
    slots = data.get("slots", [])
    selected = next((s for s in slots if s["id"] == slot_id), None)

    if not selected:
        await callback.answer("Expired. Refresh.", show_alert=True)
        return

    metrics.hits += 1
    metrics.claims_attempted += 1
    # simulated success for now
    metrics.claims_success += 1

    text = (
        f"✅ <b>CLAIMED (DEVIL)</b>\n\n"
        f"📅 {selected['date']} {selected['time']}\n"
        f"📍 {selected['city']}\n"
        f"🛂 {selected['visa_type']} — {selected['category']}\n"
        f"Score: {selected.get('score', 0)}\n\n"
        f"In full live mode this triggers multi-account claim."
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.clear()
    await callback.answer()
