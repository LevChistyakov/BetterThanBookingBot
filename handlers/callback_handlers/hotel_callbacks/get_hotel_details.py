from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from utils.named_tuples import HotelInfo
from states.bot_states import GetHotels
from rapidapi.parse_responses.find_hotels import get_hotels_info
from rapidapi.create_messages.get_hotel import create_hotel_message
from utils.search_waiting import send_waiting_message, del_waiting_messages
from loader import dp, bot


@dp.callback_query_handler(lambda call: call.data.startswith('get_hotel_map'))
async def get_hotel_map(call: CallbackQuery):
    latitude, longitude = map(float, call.data.lstrip('get_hotel_map').split('/'))

    show_in_gmaps = InlineKeyboardMarkup()
    gmaps_link = f'http://maps.google.com/maps?q={latitude},{longitude}'
    show_in_gmaps.add(InlineKeyboardButton('Открыть в google maps', url=gmaps_link))
    await bot.send_location(chat_id=call.message.chat.id, latitude=latitude, longitude=longitude,
                            reply_markup=show_in_gmaps)

