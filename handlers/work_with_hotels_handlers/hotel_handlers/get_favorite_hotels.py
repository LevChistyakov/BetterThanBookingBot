from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from database.favorites.get_favorites import get_favorite_hotels
from database.favorites.add_favorite import add_to_favorites
from database.favorites.delete_from_favorites import delete_from_favorites

from states.bot_states import Favorite
from handlers.default_handlers.start import go_home
from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
from utils.named_tuples import HotelMessage
from loader import dp


@dp.message_handler(lambda message: message.text == '⭐️ Избранное', state='*')
async def show_favorite_hotels(message: Message, state: FSMContext):
    await Favorite.show_favorite_hotels.set()

    favorite_hotels: list[HotelMessage] = await get_favorite_hotels(message=message)
    if favorite_hotels:
        await message.answer('Избранные отели:', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Список избранного пуст')
        await go_home(message=message, state=state)
        return

    for hotel in favorite_hotels:
        await message.bot.send_photo(chat_id=message.chat.id,
                                     photo=hotel.photo,
                                     caption=hotel.text,
                                     reply_markup=hotel.buttons)


@dp.callback_query_handler(lambda call: call.data == 'add_to_favorites', state='*')
async def add_hotel_to_favorites(call: CallbackQuery):
    await add_to_favorites(message=call.message)
    await call.answer('Добавлено в избранное!', show_alert=True)
    await call.message.edit_reply_markup(edit_hotel_keyboard_by_favorite(current_keyboard=call.message.reply_markup,
                                                                         is_favorite=True))


@dp.callback_query_handler(lambda call: call.data == 'delete_from_favorites', state='*')
async def delete_hotel_from_favorites(call: CallbackQuery, state: FSMContext):
    await delete_from_favorites(message=call.message)
    await call.answer('Удалено из избранного!', show_alert=True)
    await call.message.edit_reply_markup(edit_hotel_keyboard_by_favorite(current_keyboard=call.message.reply_markup,
                                                                         is_favorite=False))

    current_state = await state.get_state()
    if current_state == Favorite.show_favorite_hotels.state:
        await call.message.delete()
