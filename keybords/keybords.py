from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_today = KeyboardButton('Сегодня')
button_tomorrow = KeyboardButton('Завтра')
button_next_week = KeyboardButton('Через неделю')

date_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_today,
                                                        button_tomorrow,
                                                        button_next_week)
