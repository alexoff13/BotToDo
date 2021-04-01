# from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

bot = Bot(token='TOKEN', parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(port=7777)
dp = Dispatcher(bot, storage=storage)
