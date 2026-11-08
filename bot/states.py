from aiogram.fsm.state import State, StatesGroup

class BookingStates(StatesGroup):
    choosing_country = State()
    choosing_city = State()
    choosing_visa_type = State()
    choosing_category = State()
    confirming_slot = State()
