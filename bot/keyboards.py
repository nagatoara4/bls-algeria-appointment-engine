from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

COUNTRIES = ["Spain", "Italy", "France", "Germany", "Portugal", "Belgium"]
CITIES = ["ALG1", "ALG2", "ALG3", "ALG4", "ORAN1", "ORAN2", "ORAN3", "ORAN4"]
VISA_TYPES = ["C - Short Stay", "D - Long Stay"]
CATEGORIES_C = ["Tourism", "Business", "Family Visit", "Medical"]
CATEGORIES_D = ["Study", "Work", "Family Reunion"]

def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Start Booking")],
            [KeyboardButton(text="📡 Monitor"), KeyboardButton(text="📊 Status")],
            [KeyboardButton(text="❌ Cancel")],
        ],
        resize_keyboard=True
    )

def countries_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=c, callback_data=f"country:{c}")] for c in COUNTRIES
    ])

def cities_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=c, callback_data=f"city:{c}")] for c in CITIES
    ])

def visa_types_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=v, callback_data=f"visa:{v}")] for v in VISA_TYPES
    ])

def categories_kb(visa_type: str) -> InlineKeyboardMarkup:
    cats = CATEGORIES_C if visa_type.startswith("C") else CATEGORIES_D
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=c, callback_data=f"cat:{c}")] for c in cats
    ])

def slots_kb(slots: list) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{s['date']} {s['time']} ★{s.get('score', 0)}", callback_data=f"slot:{s['id']}")]
        for s in slots
    ]
    buttons.append([InlineKeyboardButton(text="🔄 Refresh", callback_data="refresh_slots")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
