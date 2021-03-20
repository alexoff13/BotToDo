from datetime import datetime

from aiogram import types

from loader import dp
from models import Task
from utils import db


@dp.message_handler(commands='today')
async def enter_test(message: types.Message):
    d = datetime.today().date()
    tasks = db.get_date_tasks(f'{d.day} {d.month} {d.year % 100}', message.from_user.id)
    await message.answer('Задачи на сегодня:\n')
    for i, task in enumerate(tasks):
        await message.answer(f'{i}. {Task(*task).__str__()}')
