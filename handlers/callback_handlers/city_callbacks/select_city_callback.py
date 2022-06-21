from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from loader import dp
from states.bot_states import SelectCity
from handlers.callback_handlers.date_callbacks.date_select_callbacks import start_select_date_in


@dp.callback_query_handler(state=SelectCity.select_city)
async def set_city_id(call: CallbackQuery, state: FSMContext):
    city_id = call.data.lstrip('search_in_city')
    await state.update_data(city_id=city_id)

    await call.answer('Город выбран', show_alert=False)
    await call.message.edit_text('Город выбран!', reply_markup=None)

    await start_select_date_in(call=call)
