from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiohttp import ClientSession

from config_data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

# session = create_session(url='https://hotels4.p.rapidapi.com')
session = ClientSession('https://hotels4.p.rapidapi.com')
