from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):
    waiting_email = State()
    waiting_password = State()
    choosing_country = State()
    choosing_city = State()
    choosing_visa_type = State()
    choosing_category = State()
    scanning_slots = State()
    confirming_slot = State()
    filling_details = State()
