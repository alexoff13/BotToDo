from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from states import GetTask


@dp.message_handler(commands='cancel', state="*")
async def bot_cancel(message: types.Message, state:FSMContext):
    await state.reset_state(with_data=True)
    await message.answer('Состояния сброшены')


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/start - Начать диалог",
            "/add - Добавить новую задачу",
            "/get - Получить списки задач",
            "/help - Получить справку")

    await message.answer("\n".join(text))
