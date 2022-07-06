from aiogram.dispatcher.filters.state import StatesGroup, State


class SelectCity(StatesGroup):
    wait_city_name = State()
    select_city = State()


class SelectDates(StatesGroup):
    start_select_date_in = State()
    select_date_in = State()

    start_select_date_out = State()
    select_date_out = State()

    is_date_correct = State()


class GetHotels(StatesGroup):
    is_info_correct = State()
    get_hotels_menu = State()

