from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

import keybords
from loader import dp
from models.parse_date import parse_date
from states import AddTask
from utils import db, set_new_at_job


@dp.message_handler(commands='add')
async def add_task(message: types.Message):
    await message.answer('Введите название задачи:\n')

    await AddTask.AddName.set()


@dp.message_handler(state=AddTask.AddName)
async def add_name(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer("Введите дату выполнения задачи в формате dd mm yy",
                         reply_markup=keybords.add_date_in_task)
    await AddTask.AddDate.set()


@dp.message_handler(state=AddTask.AddDate)
async def add_date_from_text(message: types.Message, state: FSMContext):
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
    await message.answer("Добавьте текстовое описание задачи: ",
                         reply_markup=keybords.description)
    await AddTask.AddDescription.set()


@dp.callback_query_handler(keybords.add_date_callback.filter(), state=AddTask.AddDate)
async def add_date(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    call.message.text = callback_data.get('date')
    await add_date_from_text(call.message, state)


@dp.callback_query_handler(keybords.inline_data_callback.add_description_callback.filter(description='false'),
                           state=AddTask.AddDescription)
async def skip_description(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    name = data.get('name')
    date = data.get('date')
    db.add_task(call.from_user.id, name, date, ' ')
    await call.message.answer('Вы успешно добавили задачу!\n'
                              f'Название : {name}\n'
                              f'Выполнить до : {date.replace(" ", "/")}\n')
    await call.message.answer("Если хотите добавить уведомление напишите время в формате HH:MM: ",
                              reply_markup=keybords.cancel)
    await AddTask.AddNotification.set()


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
    await message.answer("Если хотите добавить уведомление напишите время в формате HH:MM: ",
                         reply_markup=keybords.cancel)
    await AddTask.AddNotification.set()


@dp.callback_query_handler(state=AddTask.AddNotification.set())  # вызовется если пользователь не будет добавлять
async def exit_the_view(call: CallbackQuery, state: FSMContext):  # уведомление
    await call.answer(cache_time=60)
    await state.reset_state()


@dp.message_handler(state=AddTask.AddNotification)  # добавляем уведомление
async def add_notification(message: types.Message, state: FSMContext):
    time_ = message.text
    data = await state.get_data()
    date_ = data.get('date')
    date_at = "{} {}.{}.20{}".format(time_, *date_.split())
    name = data.get('name')
    description = data.get('description')
    text = 'Напоминаю!\n' \
           f'Название : {name}\n' \
           f'Выполнить до : {date_.replace(" ", "/")}\n' \
           f'Описание : {description}'

    set_new_at_job(message.from_user.id, date_at, text)

    await state.reset_state()
