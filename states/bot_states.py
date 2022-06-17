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
    continue_with_city = State()
    not_found = State()


class SelectDates(StatesGroup):
    pass
