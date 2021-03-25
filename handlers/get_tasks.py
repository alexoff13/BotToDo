from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageTextIsEmpty

from keybords import keybords
from loader import dp
from models import Task
from models.parse_date import parse_date
from states import GetTask
from utils import db


#  TODO Сделать кнопочки на всех этапах получения задачи
@dp.message_handler(commands='get')
async def get_input_date(message: types.Message):
    await GetTask.GetTasks.set()
    await message.answer('Сегодня/Завтра/Все', reply_markup=keybords.get_tasks)


@dp.callback_query_handler(state=GetTask.GetTasks)
async def get_tasks(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    text = call.data.lower()
    print(text)
    if text == 'сегодня' or text == 'завтра':
        delta = timedelta(days=0) if text == 'сегодня' else timedelta(days=1)
        d = datetime.today().date() + delta
        tasks = db.get_date_tasks(d.strftime('%d %m %y'),
                                  call.message.from_user.id)
    elif text == 'все':
        tasks = db.get_all_task(call.message.from_user.id)
    else:
        await call.message.answer('Попробуйте ещё раз')
        return

    try:
        await call.message.answer(f'Задачи на {text}:\n')
        await call.message.answer('\n'.join((f'{i + 1}. {Task(*task)}' for i, task in enumerate(tasks))))
    except MessageTextIsEmpty:
        await call.message.answer('Поздравляю! На сегодня задач нет')
        await state.reset_state()
        return
    await state.update_data(tasks=tasks)
    await state.update_data(date_get_task=call.data)
    await GetTask.ViewTask.set()
    await call.message.answer(f'Чтобы посмотреть описание конкретной задачи '
                              f'введите её номер: 1 - {len(tasks)}, иначе введите 0')


@dp.message_handler(state=GetTask.ViewTask)
async def view_task(message: types.Message, state: FSMContext):
    if message.text == '0':
        await state.reset_state()
        return
    data = await state.get_data()
    try:
        task = Task(*(data.get('tasks')[int(message.text.strip()) - 1]))
    except:
        await message.answer('Попробуйте ещё раз')
        return
    await message.answer('\n'.join((str(task), db.get_description(task.description_id)[1])),
                         reply_markup=keybords.action_tasks)
    await state.update_data(id_done_task=task.id)
    await GetTask.DoneTask.set()


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='done'),
                           state=GetTask.DoneTask)
async def done_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    data = await state.get_data()
    id_done_task = data.get('id_done_task')
    db.remove_task(id_done_task)
    await call.message.answer('Задача успешно выполнена')
    await state.reset_state()


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='back'),
                           state=GetTask.DoneTask)
async def return_back(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await GetTask.GetTasks.set()
    data = await state.get_data()
    call.data = data.get('date_get_task')
    await get_tasks(call, state)


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='edit'),
                           state=GetTask.DoneTask)
async def edit_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer('Какое поле вы хотите редактировать?', reply_markup=keybords.edit_task)


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='name'),
                           state=GetTask.DoneTask)
async def edit_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer('Введите новое название')
    await GetTask.EditName.set()


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='date'),
                           state=GetTask.DoneTask)
async def edit_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer('Введите новую дату')
    await GetTask.EditDate.set()


@dp.callback_query_handler(keybords.edit_task_callback.filter(action='description'),
                           state=GetTask.DoneTask)
async def edit_task(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.answer('Введите новое описание')
    await GetTask.EditDescription.set()


@dp.message_handler(state=GetTask.EditName)
async def edit_task_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_task = data.get('id_done_task')
    db.update_task_name(id_task, message.text)
    await state.reset_state()


@dp.message_handler(state=GetTask.EditDescription)
async def edit_task_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_task = data.get('id_done_task')
    task = Task(*(data.get('tasks')[id_task]))
    db.update_task_description(task.description_id, message.text)
    await state.reset_state()


@dp.message_handler(state=GetTask.EditDate)
async def edit_task_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id_task = data.get('id_done_task')
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

    db.update_task_date(id_task, answer)
    await state.reset_state()

#
#
#
# @dp.message_handler(state=GetTask.EditDate)
# @dp.message_handler(state=GetTask.EditDescription)
