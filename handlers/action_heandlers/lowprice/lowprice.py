from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from states.lowprice_states import LowPriceStates

from loader import dp


@dp.message_handler(commands='lowprice')
async def lowprice_command(message: Message):
    await message.answer('Отправьте боту город для поиска')
    await LowPriceStates.city_to_search.set()


@dp.message_handler(state=LowPriceStates.city_to_search)
async def set_city(message: Message, state: FSMContext):
    city = message.text
    await state.update_data(city=city)

    await message.answer('Какое количество отелей выводить?')
    await LowPriceStates.hotels_value.set()


@dp.message_handler(state=LowPriceStates.hotels_value)
async def set_hotels_value(message: Message, state: FSMContext):
    hotels_value = message.text
    await state.update_data(hotels_value=hotels_value)

    await message.answer('Нужны ли фото отеля?')
    await LowPriceStates.is_photo_requiered.set()


@dp.message_handler(state=LowPriceStates.is_photo_requiered)
async def photo_choice(message: Message, state: FSMContext):
    is_photo_requiered = message.text
    await state.update_data(is_photo_requiered=is_photo_requiered)

    if is_photo_requiered == 'Да':
        await message.answer('Сколько фото требуется для каждого отеля?')
        await LowPriceStates.photos_value.set()

    elif is_photo_requiered == 'Нет':
        await send_lowprice_info(message, state)
        await state.finish()


@dp.message_handler(state=LowPriceStates.photos_value)
async def set_photos_value(message: Message, state: FSMContext):
    photos_value = message.text
    await state.update_data(photos_value=photos_value)

    await send_lowprice_info(message, state)
    await state.finish()


async def send_lowprice_info(message: Message, state: FSMContext):
    data = await state.get_data()
    text = f'Город для поиска: {data.get("city")}\n' \
           f'Количество отелей для поиска: {data.get("hotels_value")}\n' \
           f'Нужны ли фото отелей: {data.get("is_photo_requiered")}\n' \
           f'Количество фото: {data.get("photos_value")}'
    await message.answer(text)
