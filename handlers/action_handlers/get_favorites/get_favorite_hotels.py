from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from database.favorites.get_favorites import get_favorite_hotels
from database.favorites.add_favorite import add_to_favorites
from database.favorites.delete_from_favorites import delete_from_favorites
from database.utils.utils import is_favorites_are_over

from states.bot_states import Favorite
from keyboards.inline.hotel_keyboards.hotel_keyboard import edit_hotel_keyboard_by_favorite
from utils.named_tuples import HotelMessage
from utils.work_with_errors import finish_with_error
from handlers.work_with_hotels_handlers.hotel_handlers.get_hotels import trying_to_send_with_photo
from loader import dp


@dp.message_handler(lambda message: message.text == '⭐️ Избранное', state='*')
async def show_favorite_hotels(message: Message, state: FSMContext):
    await Favorite.show_favorite_hotels.set()

    favorite_hotels: list[HotelMessage] = await get_favorite_hotels(message=message)
    if favorite_hotels:
        to_delete = await message.answer('Избранные отели:', reply_markup=ReplyKeyboardRemove())
        await state.update_data(favorite_message_to_delete=to_delete)
    else:
        await finish_with_error(message=message, error='favorites_empty', state=state)
        return

    for hotel in favorite_hotels:
        await trying_to_send_with_photo(message_from_user=message, hotel_message=hotel)


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

        is_favorites_are_over_ = await is_favorites_are_over(message=call.message)
        if is_favorites_are_over_:
            state_data = await state.get_data()
            message_to_delete: Message = state_data.get('favorite_message_to_delete')
            await finish_with_error(message=call.message, error='favorites_empty', state=state,
                                    to_delete=message_to_delete)
