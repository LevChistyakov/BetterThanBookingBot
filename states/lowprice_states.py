from aiogram.dispatcher.filters.state import StatesGroup, State


class LowPriceStates(StatesGroup):
    city_to_search = State()      # str
    hotels_value = State()        # int
    is_photo_requiered = State()  # bool

    photos_value = State()        # int

