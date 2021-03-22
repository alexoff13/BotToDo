# from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

bot = Bot(token='1679438623:AAHEhDonSfN08ZYbB3svi95rOh9R9hucsZg', parse_mode=types.ParseMode.HTML)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)
