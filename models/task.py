from utils import db


class Description:
    def __init__(self, text, media=None):
        self.media = media
        self.text = text


class Task:
    def __init__(self, id: int, id_user: int, name: str, date: str, description_id: int):
        self.description_id = description_id
        self.date = date
        self.name = name
        self.id_user = id_user
        self.id = id

    def __str__(self):
        date = self.date.split()
        return f'{self.name} до {date[0]}/{date[1]}/{date[2]}'

    def return_data(self):
        return self.id_user, self.name, self.date, db.get_description(self.description_id)
