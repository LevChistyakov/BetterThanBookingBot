from aiogram.dispatcher.filters.state import StatesGroup, State


class LowPriceStates(StatesGroup):
    city_to_search = State()


class HighPriceStates(StatesGroup):
    city_to_search = State()


class BestDealStates(StatesGroup):
    city_to_search = State()


class SelectCity(StatesGroup):
    wait_city_name = State()
    select_city = State()


class SelectDates(StatesGroup):
    start_select_date_in = State()
    select_date_in = State()

    start_select_date_out = State()
    select_date_out = State()

    is_date_correct = State()

