from typing import NamedTuple
from datetime import date
from aiogram.types.inline_keyboard import InlineKeyboardMarkup

KM = float
USD = float
Link = str
ID = int


class HotelInfo(NamedTuple):
    name: str
    address: str
    distance_from_center: KM
    total_cost: USD
    cost_by_night: USD


class HotelMessage(NamedTuple):
    message: str
    buttons: InlineKeyboardMarkup


class SearchInfo(NamedTuple):
    hotel_id: str
    km_to_center: KM
    date_in: date
    date_out: date
