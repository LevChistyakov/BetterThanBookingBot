from aiogram.dispatcher import FSMContext
from aiogram.types.message import Message
from aiogram.types.callback_query import CallbackQuery

from utils.named_tuples import SearchInfo
from states.bot_states import GetHotels
from rapidapi.create_messages.get_hotel import create_hotel_message
from rapidapi.parse_responses.find_hotels import get_hotels_info
from utils.search_waiting import send_waiting_message, del_waiting_messages
from loader import dp, bot


@dp.callback_query_handler(state=GetHotels.is_info_correct)
async def is_info_correct(call: CallbackQuery, state: FSMContext):
    message = call.message
    if call.data == 'city_info_correct':
        await message.delete()
        text_to_delete, sticker_to_delete = await send_waiting_message(message)

        state_data = await state.get_data()
        hotels_info = await get_hotels_info(data=state_data)
        await state.update_data(hotels_info=hotels_info)

        date_in, date_out = state_data.get('date_in'), state_data.get('date_out')
        hotel_id, hotel_km, hotel_photo = hotels_info[0]['id'], hotels_info[0]['km'], hotels_info[0]['photo']
        to_search = SearchInfo(hotel_id=hotel_id, km_to_center=hotel_km, date_in=date_in, date_out=date_out)
        hotel_message, hotel_markup = await create_hotel_message(hotel_info_for_search=to_search)

        await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
        await bot.send_photo(chat_id=message.chat.id, photo=hotel_photo, caption=hotel_message,
                             reply_markup=hotel_markup)
        await state.update_data(hotel_index=1)
        await GetHotels.get_hotels_menu.set()

    elif call.data == 'city_info_incorrect':
        pass


@dp.message_handler(state=GetHotels.get_hotels_menu)
async def show_new_hotel(message: Message, state: FSMContext):
    text_to_delete, sticker_to_delete = await send_waiting_message(message)

    state_data = await state.get_data()
    print(state_data)

    hotel_index = state_data.get('hotel_index')
    hotel = state_data.get('hotels_info')[hotel_index]

    date_in, date_out = state_data.get('date_in'), state_data.get('date_out')
    hotel_id, hotel_km, hotel_photo = hotel['id'], hotel['km'], hotel['photo']
    to_search = SearchInfo(hotel_id=hotel_id, km_to_center=hotel_km, date_in=date_in, date_out=date_out)
    hotel_message, hotel_markup = await create_hotel_message(hotel_info_for_search=to_search)

    await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
    await bot.send_photo(chat_id=message.chat.id, photo=hotel_photo, caption=hotel_message, reply_markup=hotel_markup)
    await state.update_data(hotel_index=hotel_index + 1)
    await GetHotels.get_hotels_menu.set()


