from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

import keybords
from loader import dp
from models.parse_date import parse_date
from states import AddTask
from utils import db


# TODO возможность редактировать данные в процессе добавления


@dp.message_handler(commands='add')
async def add_task(message: types.Message):
    await message.answer('Введите название задачи:\n')

    await AddTask.AddName.set()


@dp.message_handler(state=AddTask.AddName)
async def add_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("Введите дату выполнения задачи в формате dd mm yy",
                         reply_markup=keybords.date_kb)
    await AddTask.AddDate.set()


@dp.message_handler(state=AddTask.AddDate)
async def add_date(message: types.Message, state: FSMContext):
    # TODO добавлять дату с разными разделителями
    answer = message.text
    try:
        if answer.isalpha():
            answer = parse_date(answer)
        else:
            date = datetime.strptime(answer.strip(), "%d %m %y")
            if date.date() < datetime.today().date():
                await message.answer("Дата меньше текущей")
                raise ValueError('Дата меньше текущей')
    except ValueError:
        await message.answer("Попробуйте ещё раз.\nВведите дату"
                             " выполнения задачи в формате dd mm yy")
        return

    await state.update_data(date=answer)
    await message.answer("Добавьте текстовое описание задачи: ", reply_markup=ReplyKeyboardRemove())
    await AddTask.AddDescription.set()


@dp.message_handler(state=AddTask.AddDescription)
async def add_description(message: types.Message, state: FSMContext):
    answer = message.text

    await state.update_data(description=answer)
    data = await state.get_data()
    name = data.get('name')
    date = data.get('date')
    description = data.get('description')
    db.add_task(message.from_user.id, name, date, description)
    await message.answer('Вы успешно добавили задачу!\n'
                         f'Название : {name}\n'
                         f'Выполнить до : {date.replace(" ", "/")}\n'
                         f'Описание : {description}')
    await state.reset_state()
