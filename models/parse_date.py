from datetime import datetime, timedelta


def parse_date(message: str):
    d = datetime.today().date()
    weekdays = {'Пн': 1,
                'Вт': 2,
                'Ср': 3,
                'Чт': 4,
                'Пт': 5,
                'Сб': 6,
                'Вс': 0,
                }
    if message == 'Сегодня':
        return f'{d.day} {d.month} {d.year % 100}'
    if message == 'Завтра':
        d += timedelta(days=1)
        return f'{d.day} {d.month} {d.year % 100}'
    if message == 'ЧерезНеделю':
        d += timedelta(days=7)
        print(d)
        return f'{d.day} {d.month} {d.year % 100}'
    if message in weekdays.keys():
        d += timedelta(days=abs(d.weekday() - weekdays[message]))
        return f'{d.day} {d.month} {d.year % 100}'
    raise ValueError('Неизвестное сокращение')
