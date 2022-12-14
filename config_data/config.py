import os
from dotenv import load_dotenv, find_dotenv

import datetime

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
MONGO_DB_USERNAME = os.getenv('MONGO_DB_USERNAME')
MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')

time_offset = datetime.timezone(datetime.timedelta(hours=3))

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Топ самых  дешевых отелей"),
    ('highprice', "Топ самых  дорогих отелей"),
    ('bestdeal', "Выбор отеля с условиями"),
    ('history', 'История поиска'),
    ('favorites', 'Избранное')
)
