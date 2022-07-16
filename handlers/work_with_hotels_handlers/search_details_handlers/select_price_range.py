from aiogram.types.callback_query import CallbackQuery, Message
from aiogram.dispatcher import FSMContext

from keyboards.inline.bestdeal.select_keyboards import price_range_keyboard
from states.bot_states import BestDeal
from utils.named_tuples import USD

from .select_distance_range import start_select_distance_range
from utils.delete_messages import delete_errors_messages
from loader import dp


async def start_select_price_range(call: CallbackQuery, state: FSMContext):
    await state.update_data(min_price=None, max_price=None)
    await BestDeal.select_price_range.set()
    await call.message.answer('<b>Укажите диапазон цены за ночь</b>', reply_markup=price_range_keyboard())


@dp.callback_query_handler(lambda call: call.data == 'select_min_price', state=BestDeal.select_price_range)
async def send_min_price_request(call: CallbackQuery, state: FSMContext):
    message = await call.message.answer('<b>Отправьте минимальную цену в $</b>\n'
                                        'Пример: <b>100</b> или <b>50.25</b>')
    await state.update_data(message_to_delete=message)
    await state.update_data(errors_messages=[])
    await state.update_data(message_to_edit=call.message)
    await BestDeal.wait_min_price.set()


@dp.message_handler(state=BestDeal.wait_min_price)
async def get_min_price(message: Message, state: FSMContext):
    state_data = await state.get_data()
    errors: list[Message] = state_data.get('errors_messages')
    try:
        price: USD = float(message.text)
    except ValueError:
        error_message = await message.answer('<b>❗️Отправьте боту число!</b>')
        errors.extend([error_message, message])
        await state.update_data(errors_messages=errors)
        return

    max_price = state_data.get('max_price')
    if max_price is not None:
        if max_price < price:
            error_message = await message.answer('<b>❗️Минимальная стоимость должна быть меньше максимальной!</b>')
            errors.extend([error_message, message])
            await state.update_data(errors_messages=errors)
            return

    messsage_from_bot: Message = state_data.get('message_to_delete')
    messsage_from_user: Message = message

    message_with_select_price: Message = state_data.get('message_to_edit')
    await messsage_from_bot.delete()
    await messsage_from_user.delete()

    await state.update_data(min_price=price)
    await delete_errors_messages(message_list=errors)
    await state.update_data(errors_messages=[])
    await edit_price_message(message_to_edit=message_with_select_price, state=state)
    await BestDeal.select_price_range.set()


@dp.callback_query_handler(lambda call: call.data == 'select_max_price', state=BestDeal.select_price_range)
async def send_max_price_request(call: CallbackQuery, state: FSMContext):
    message = await call.message.answer('<b>Отправьте максимальную цену в $</b>\n'
                                        'Пример: <b>100</b> или <b>50.25</b>')
    await state.update_data(message_to_delete=message)
    await state.update_data(message_to_edit=call.message)
    await BestDeal.wait_max_price.set()


@dp.message_handler(state=BestDeal.wait_max_price)
async def get_max_price(message: Message, state: FSMContext):
    state_data = await state.get_data()
    errors: list[Message] = state_data.get('errors_messages')

    try:
        price: USD = float(message.text)
    except ValueError:
        error_message = await message.answer('<b>Отправьте боту число!</b>')
        errors.extend([error_message, message])
        await state.update_data(errors_messages=errors)
        return

    min_price = state_data.get('min_price')
    if min_price is not None:
        if min_price > price:
            error_message = await message.answer('<b>❗️Максимальная стоимость должна быть больше минимальной!</b>')
            errors.extend([error_message, message])
            await state.update_data(errors_messages=errors)
            return

    messsage_from_bot: Message = state_data.get('message_to_delete')
    messsage_from_user: Message = message

    message_with_select_price: Message = state_data.get('message_to_edit')
    await messsage_from_bot.delete()
    await messsage_from_user.delete()

    await state.update_data(max_price=price)
    await delete_errors_messages(message_list=errors)
    await state.update_data(errors_messages=[])
    await edit_price_message(message_to_edit=message_with_select_price, state=state)
    await BestDeal.select_price_range.set()


@dp.callback_query_handler(lambda call: call.data == 'end_price_range', state=BestDeal.select_price_range)
async def end_price_range_selecting(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    if state_data.get('min_price') is None:
        await state.update_data(min_price=0)
    elif state_data.get('max_price') is None:
        await state.update_data(max_price=1000)

    await call.message.edit_text('<b>💲 Диапазон цен выбран!</b>')
    await start_select_distance_range(call, state)


async def edit_price_message(message_to_edit: Message, state: FSMContext):
    state_data = await state.get_data()
    min_price, max_price = state_data.get('min_price'), state_data.get('max_price')

    if min_price is not None and max_price is not None:
        text = f'<b>Укажите диапазон цены за ночь</b>\n' \
               f'Минимальная цена: <b>{min_price} $</b>\n' \
               f'Максимальная цена: <b>{max_price} $</b>'
    elif max_price is None:
        text = f'<b>Укажите диапазон цены за ночь</b>\n' \
               f'Минимальная цена: <b>{min_price} $</b>'
    elif min_price is None:
        text = f'<b>Укажите диапазон цены за ночь</b>\n' \
               f'Максимальная цена: <b>{max_price} $</b>'

    await message_to_edit.edit_text(text=text, reply_markup=price_range_keyboard())
