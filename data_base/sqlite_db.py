import sqlite3 as sq


class DataBase:

    def __init__(self, db_name):
        self.__base = sq.connect(db_name)
        self.__cur = self.__base.cursor()
        if self.__base:
            print('База данных подключена')

    def create_table(self, name: str):
        self.__cur.execute("CREATE TABLE IF NOT EXISTS {name}(command,time PRIMARY KEY, hotel_description)".format(name=name))
        self.__base.commit()

    def insert(self, name: str, command: str, time: str, description: str):
        self.create_table(name)
        count = int(self.__cur.execute('SELECT COUNT(*) FROM {name}'.format(name=name)).fetchone()[0])

        if count >= 15:
            self.__cur.execute('DELETE FROM {name}'.format(name=name))
            self.__base.commit()
        self.__cur.execute('INSERT INTO {name} VALUES(?, ?, ?)'.format(name=name),
                           (command, time, description))
        self.__base.commit()

    def get_values(self, name: str):
        response = self.__cur.execute('SELECT * FROM {name}'.format(name=name))
        self.__base.commit()
        return response
