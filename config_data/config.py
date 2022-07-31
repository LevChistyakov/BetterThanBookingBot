import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
MONGO_DB_PASSWORD = os.getenv('MONGO_DB_PASSWORD')

headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Топ самых  дешевых отелей"),
    ('highprice', "Топ самых  дорогих отелей"),
    ('bestdeal', "Выбор отеля с условиями"),
    ('history', 'История поиска')
)
