from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states import BookingStates
from bot.keyboards import (
    countries_kb, cities_kb, visa_types_kb,
    categories_kb, slots_kb, main_menu
)
from bot.services.slots import generate_slots
from bot.services.session import update_session, get_session
from bot.services.storage import increment_booking

router = Router()

@router.message(F.text == "🚀 Start Booking")
async def start_booking(message: Message, state: FSMContext):
    await state.set_state(BookingStates.choosing_country)
    await message.answer(
        "Select destination country:",
        reply_markup=countries_kb()
    )

@router.callback_query(F.data.startswith("country:"))
async def on_country(callback: CallbackQuery, state: FSMContext):
    country = callback.data.split(":", 1)[1]
    await state.update_data(country=country)
    await state.set_state(BookingStates.choosing_city)
    await callback.message.edit_text(
        f"Country: <b>{country}</b>\n\nSelect BLS center:",
        reply_markup=cities_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("city:"))
async def on_city(callback: CallbackQuery, state: FSMContext):
    city = callback.data.split(":", 1)[1]
    await state.update_data(city=city)
    await state.set_state(BookingStates.choosing_visa_type)
    await callback.message.edit_text(
        f"Center: <b>{city}</b>\n\nSelect visa type:",
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
    await state.update_data(category=category)
    data = await state.get_data()

    await callback.message.edit_text("🔍 Scanning available slots...")
    slots = generate_slots(
        city=data["city"],
        visa_type=data["visa_type"],
        category=category
    )
    await state.update_data(slots=slots)
    await state.set_state(BookingStates.confirming_slot)

    if not slots:
        await callback.message.edit_text("No slots found right now. Try again later.")
        await callback.answer()
        return

    text = (
        f"✅ Found {len(slots)} slots\n"
        f"Country: {data['country']} | Center: {data['city']}\n"
        f"Visa: {data['visa_type']} | Category: {category}\n\n"
        f"Select a slot:"
    )
    await callback.message.edit_text(text, reply_markup=slots_kb(slots))
    await callback.answer()

@router.callback_query(F.data == "refresh_slots")
async def refresh_slots(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    slots = generate_slots(
        city=data.get("city", "ALG1"),
        visa_type=data.get("visa_type", "C - Short Stay"),
        category=data.get("category", "Tourism")
    )
    await state.update_data(slots=slots)
    await callback.message.edit_text(
        f"🔄 Refreshed — {len(slots)} slots:\n\nSelect one:",
        reply_markup=slots_kb(slots)
    )
    await callback.answer("Refreshed")

@router.callback_query(F.data.startswith("slot:"))
async def on_slot(callback: CallbackQuery, state: FSMContext):
    slot_id = callback.data.split(":", 1)[1]
    data = await state.get_data()
    slots = data.get("slots", [])
    selected = next((s for s in slots if s["id"] == slot_id), None)

    if not selected:
        await callback.answer("Slot expired. Refresh.", show_alert=True)
        return

    await state.update_data(selected_slot=selected)
    increment_booking(callback.from_user.id)

    text = (
        f"✅ <b>Slot reserved (simulation)</b>\n\n"
        f"📅 {selected['date']} at {selected['time']}\n"
        f"📍 {selected['city']}\n"
        f"🛂 {selected['visa_type']} — {selected['category']}\n\n"
        f"In a real deployment this would proceed to form fill + payment.\n"
        f"You can extend the services layer with real portal automation."
    )
    await callback.message.edit_text(text, parse_mode="HTML")
    await state.clear()
    await callback.answer()
