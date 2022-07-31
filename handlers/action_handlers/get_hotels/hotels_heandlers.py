from aiogram.types.message import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from database.history.update_history import add_command_to_history
from datetime import datetime
from states.bot_states import SelectCity
from loader import dp


@dp.message_handler(Command(['lowprice', 'highprice', 'bestdeal']), state='*')
async def define_state(message: Message, state: FSMContext):
    """"Catches lowprice and higprice commands. Asks user for city name"""

    await message.answer('<b>↘️ Отправьте боту город для поиска</b>', reply_markup=ReplyKeyboardRemove())
    await SelectCity.wait_city_name.set()

    command = message.text.lstrip('/')
    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['Топ недорогих отелей']), state='*')
async def show_lowprice(message: Message, state: FSMContext):
    """"Catches text about lowprice hotels. Asks user for city name"""

    await message.answer('<b>↘️ Отправьте боту город для поиска</b>', reply_markup=ReplyKeyboardRemove())
    await SelectCity.wait_city_name.set()

    command = 'lowprice'
    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['Топ дорогих отелей']), state='*')
async def show_highprice(message: Message, state: FSMContext):
    """"Catches text about highprice hotels. Asks user for city name"""

    await message.answer('<b>↘️ Отправьте боту город для поиска</b>', reply_markup=ReplyKeyboardRemove())
    await SelectCity.wait_city_name.set()

    command = 'highprice'
    await register_command_in_db(command, message, state)


@dp.message_handler(Text(['Поиск с параметрами']), state='*')
async def show_highprice(message: Message, state: FSMContext):
    """"Catches text about hotels with best deal. Asks user for city name"""

    await message.answer('<b>↘️ Отправьте боту город для поиска</b>', reply_markup=ReplyKeyboardRemove())
    await SelectCity.wait_city_name.set()

    command = 'bestdeal'
    await register_command_in_db(command, message, state)


async def register_command_in_db(command: str, message: Message, state: FSMContext):
    call_time = message.date

    await add_command_to_history(command=command, call_time=call_time, message=message)
    await state.update_data(command_type=command, command_call_time=call_time)
