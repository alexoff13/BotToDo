from datetime import datetime


class Description:
    def __init__(self, text, media=None):
        self.media = media
        self.text = text


class Task:
    def __init__(self, date: datetime, name: str, description: Description):
        self.description = description
        self.date = date
        self.name = name

    def __str__(self):
        return f'{self.name} до {self.date}'
