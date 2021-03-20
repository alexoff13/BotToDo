class Description:
    def __init__(self, text, media=None):
        self.media = media
        self.text = text


class Task:
    def __init__(self, id: int, id_user: int, name: str,  date: str, description_id: int):
        self.description_id = description_id
        self.date = date
        self.name = name
        self.id_user = id_user
        self.id = id

    def __str__(self):
        return f'{self.name} до {self.date}'
