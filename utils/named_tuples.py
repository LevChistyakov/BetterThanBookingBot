from typing import NamedTuple, Optional
from aiogram.types.inline_keyboard import InlineKeyboardMarkup

KM = float
USD = float
Link = str
ID = int
Degrees = float
Latitude = Degrees
Longitude = Degrees


class CitiesMessage(NamedTuple):
    message: str
    buttons: InlineKeyboardMarkup


class CalendarMarkupAndStep(NamedTuple):
    calendar: InlineKeyboardMarkup
    date_type: str


class HotelInfo(NamedTuple):
    hotel_id: ID
    name: str
    address: str
    distance_from_center: KM
    total_cost: USD
    cost_by_night: USD
    photo: Link
    coordinates: tuple[Latitude, Longitude]


class HotelMessage(NamedTuple):
    text: str
    photo: Link
    buttons: InlineKeyboardMarkup


class HistoryPage(NamedTuple):
    text: str
    found_hotels: list[HotelMessage]
