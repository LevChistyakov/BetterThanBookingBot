from aiogram.types.inline_keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def price_range_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    min_price_button = InlineKeyboardButton('➖ Указать от скольки', callback_data='select_min_price')
    max_price_button = InlineKeyboardButton('➕ Указать до скольки', callback_data='select_max_price')
    complete_button = InlineKeyboardButton('✅ Готово', callback_data='end_price_range')

    keyboard.add(min_price_button, max_price_button, complete_button)
    return keyboard


def distance_range_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)

    min_distance_button = InlineKeyboardButton('➖ Указать от скольки', callback_data='select_min_distance')
    max_distance_button = InlineKeyboardButton('➕ Указать до скольки', callback_data='select_max_distance')
    complete_button = InlineKeyboardButton('✅ Готово', callback_data='end_distance_range')

    keyboard.add(min_distance_button, max_distance_button, complete_button)
    return keyboard
