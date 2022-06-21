from aiogram.dispatcher import FSMContext
from aiogram.types.callback_query import CallbackQuery

from loader import dp
from states.bot_states import SelectDates
from keyboards.inline.date_keyboards.date_keyboards import CustomCalendar, CUSTOM_STEPS, create_calendar, \
    is_date_in_correct_markup, is_date_out_correct_markup, get_readble_date


async def start_select_date_in(call: CallbackQuery):
    calendar_info = create_calendar()
    await call.message.answer(f'Выберите {calendar_info.date_type} заезда', reply_markup=calendar_info.calendar)
    await SelectDates.select_date_in.set()


async def start_select_date_out(call: CallbackQuery, date_in: str):
    calendar_info = create_calendar(minimal_date=date_in)
    await call.message.answer(f'Выберите {calendar_info.date_type} выезда', reply_markup=calendar_info.calendar)
    await SelectDates.select_date_out.set()


@dp.callback_query_handler(state=SelectDates.select_date_in)
async def select_date_in(call: CallbackQuery, state: FSMContext):
    result, keyboard, step = CustomCalendar(locale='ru').process(call_data=call.data)
    if not result and keyboard:
        await call.message.edit_text(f'Укажите {CUSTOM_STEPS[step]} заезда',
                                     reply_markup=keyboard)

    elif result:
        await state.update_data(date_in=result)
        message = get_readble_date(str_date=str(result))
        await call.message.edit_text(f'Выбрано: {message}\n'
                                     f'Все верно?', reply_markup=is_date_in_correct_markup())
        await SelectDates.is_date_correct.set()


@dp.callback_query_handler(state=SelectDates.select_date_out)
async def select_date_out(call: CallbackQuery, state: FSMContext):
    result, keyboard, step = CustomCalendar(locale='ru').process(call_data=call.data)
    if not result and keyboard:
        await call.message.edit_text(f'Укажите {CUSTOM_STEPS[step]} выезда',
                                     reply_markup=keyboard)

    elif result:
        await state.update_data(date_out=result)
        message = get_readble_date(str_date=str(result))
        await call.message.edit_text(f'Выбрано: {message}\n'
                                     f'Все верно?', reply_markup=is_date_out_correct_markup())
        await SelectDates.is_date_correct.set()


@dp.callback_query_handler(state=SelectDates.is_date_correct)
async def send_confirmation_date(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    date_in = state_data.get('date_in')

    if call.data == 'date_in_correct':
        await call.answer('Укажите дату выезда', show_alert=False)
        await call.message.delete()
        await start_select_date_out(call=call, date_in=date_in)

    if call.data == 'date_in_incorrect':
        await call.answer('Попробуйте еще раз', show_alert=True)
        await call.message.delete()
        await start_select_date_in(call=call)

    if call.data == 'date_out_correct':
        await call.answer('Дата выезда указана', show_alert=False)
        await call.message.delete()
        await state.finish()

    if call.data == 'date_out_incorrect':
        await call.answer('Попробуйте еще раз', show_alert=True)
        await call.message.delete()
        await start_select_date_out(call=call, date_in=date_in)
