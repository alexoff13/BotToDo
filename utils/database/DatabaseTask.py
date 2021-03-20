import sqlite3


class DatabaseTasks:
    def __init__(self, path_to_db='files/tasks.db'):
        self.__path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.__path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False,
                fetchall=False, commit=False):
        connection = self.connection
        connection.set_trace_callback(self.__logger)
        cursor = connection.cursor()
        if parameters is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()

        connection.close()
        return data

    def create_db(self):
        with open('files/creation.txt', 'r') as infile:
            scripts = map(lambda x: x + ';', infile.read().replace('\n', '').split(';')[:-1])
        for script in scripts:
            self.execute(script, commit=True)

    def _get_last_rowid(self, table):
        return self.execute(f"SELECT * FROM {table} ORDER BY ID DESC LIMIT 1", fetchone=True)[0]

    def add_task(self, id_user: int, name: str,
                 date: str, description: str):
        sql = "INSERT INTO Descriptions(text_description) VALUES(?)"
        self.execute(sql, parameters=(description,), commit=True)

        description_id = self._get_last_rowid('Descriptions')
        sql = "INSERT INTO Tasks(id_user, name, date_, description_id) VALUES(?, ?, ?, ?)"

        parameters = (id_user, name, date, description_id)
        self.execute(sql, parameters=parameters, commit=True)

    def remove_task(self, id_: int):
        sql = f"DELETE FROM Tasks WHERE ID = {id_}"
        self.execute(sql, commit=True)

    def get_date_tasks(self, date: str, id_user):
        sql = f"SELECT * FROM Tasks WHERE date_ = \"{date}\" AND id_user = {id_user}"
        return self.execute(sql, commit=False, fetchall=True)

    @staticmethod
    def __logger(statement):
        print(f"""
    ______________________________________________________________________
    Executing:
    {statement}
    ______________________________________________________________________
    """)
