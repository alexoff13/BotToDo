from datetime import datetime, timedelta

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageTextIsEmpty

from loader import dp
from models import Task
from states import GetTask
from utils import db


#  TODO Сделать кнопочки на всех этапах получения задачи
@dp.message_handler(commands='get')
async def get_input_date(message: types.Message):
    await GetTask.GetTasks.set()
    await message.answer('Сегодня/Завтра/Все')


@dp.message_handler(state=GetTask.GetTasks)
async def get_tasks(message: types.Message, state: FSMContext):
    text = message.text.lower()
    if text == 'сегодня' or text == 'завтра':
        delta = timedelta(days=0) if text == 'сегодня' else timedelta(days=1)
        d = datetime.today().date() + delta
        tasks = db.get_date_tasks(d.strftime('%d %m %y'),
                                  message.from_user.id)
    elif text == 'все':
        tasks = db.get_all_task(message.from_user.id)
    else:
        await message.answer('Попробуйте ещё раз')
        return

    try:
        await message.answer(f'Задачи на {text}:\n')
        await message.answer('\n'.join((f'{i + 1}. {Task(*task)}' for i, task in enumerate(tasks))))
    except MessageTextIsEmpty:
        await message.answer('Поздравляю! На сегодня задач нет')
    await message.answer(f'Чтобы посмотреть описание конкретной задачи '
                         f'введите её номер: 1 - {len(tasks)}, иначе введите 0')
    await state.update_data(tasks=tasks)
    await state.update_data(date_get_task=message.text)
    await GetTask.ViewTask.set()


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
    await message.answer('\n'.join((task.__str__(), db.get_description(task.description_id)[1])))
    await message.answer('Если задача выполнена нажмите d, вернуться к списку - b')
    await state.update_data(id_done_task=task.id)
    await GetTask.DoneTask.set()


@dp.message_handler(state=GetTask.DoneTask)
async def done_task(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == 'b':
        await GetTask.GetTasks.set()
        message.text = data.get('date_get_task')
        await get_tasks(message, state)
    if message.text != 'd':
        await state.reset_state()
        return
    data = await state.get_data()
    id_done_task = data.get('id_done_task')
    db.remove_task(id_done_task)
    await state.reset_state()
