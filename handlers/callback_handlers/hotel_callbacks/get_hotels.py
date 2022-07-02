from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from utils.named_tuples import HotelInfo
from states.bot_states import GetHotels
from rapidapi.parse_responses.find_hotels import get_hotels_info
from rapidapi.create_messages.get_hotel import create_hotel_message
from utils.search_waiting import send_waiting_message, del_waiting_messages
from loader import dp, bot


@dp.callback_query_handler(state=GetHotels.is_info_correct)
async def is_info_correct(call: CallbackQuery, state: FSMContext):
    message = call.message
    if call.data == 'city_info_correct':
        await message.delete()
        text_to_delete, sticker_to_delete = await send_waiting_message(message)

        state_data = await state.get_data()
        hotels_info: list[HotelInfo] = await get_hotels_info(data=state_data)
        await state.update_data(hotels_info=hotels_info, hotel_index=1)

        hotel_info = hotels_info[0]
        hotel_message = create_hotel_message(hotel_info)
        await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
        await bot.send_photo(chat_id=message.chat.id, photo=hotel_message.photo, caption=hotel_message.text,
                             reply_markup=hotel_message.buttons)

        await GetHotels.get_hotels_menu.set()

    elif call.data == 'city_info_incorrect':
        pass


# @dp.callback_query_handler(state=GetHotels.get_hotels_menu)
# async def show_new_hotel(call: CallbackQuery, state: FSMContext):
#     text_to_delete, sticker_to_delete = await send_waiting_message(call.message)
#     state_data = await state.get_data()
#
#     hotel_index = state_data.get('hotel_index')
#     hotels_info: list[HotelInfo] = state_data.get('hotels_info')
#     hotel = hotels_info[hotel_index]
#     hotel_message = create_hotel_message(hotel_info=hotel)
#
#     await del_waiting_messages(text=text_to_delete, sticker=sticker_to_delete)
#     await bot.send_photo(chat_id=call.message.chat.id, photo=hotel_message.photo, caption=hotel_message.text,
#                          reply_markup=hotel_message.buttons)
#     await state.update_data(hotel_index=hotel_index + 1)
