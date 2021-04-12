# from os import getenv

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

bot = Bot(token='1731506104:AAFTSw03X1CIQf8zv4TJ-AHto7a0gAFRjrU', parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(port=7777)
dp = Dispatcher(bot, storage=storage)
