import sqlite3

class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ('CREATE TABLE IF NOT EXISTS users('
                     'id INTEGER PRIMARY KEY,'
                     'user_call TEXT,'
                     'user_name TEXT,'
                     'telegram_id TEXT);')
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании БД: ', Error)

    def add_user(self, user_call, user_name, telegram_id):
        self.cursor.execute(f'INSERT INTO users (user_call,user_name, telegram_id) VALUES (?, ?, ?)', (user_call,user_name, telegram_id))
        self.connection.commit()

    def add_table_user(self, user_call):
        # lotwd_db = user_call + '_LoTW'

        try:
            query = (f'''
                     CREATE TABLE IF NOT EXISTS {user_call}(
                     qso_date TEXT,
                     time_on TEXT,
                     band TEXT,
                     mode TEXT,
                     call TEXT,
                     gridsquare TEXT,
                     operator TEXT,
                     PRIMARY KEY(qso_date, time_on, band, mode, call));

                     CREATE TABLE IF NOT EXISTS {user_call+'_lotw'}(
                     qso_date TEXT,
                     time_on TEXT,
                     band TEXT,
                     mode TEXT,
                     call TEXT,
                     gridsquare TEXT,
                     operator TEXT,
                     PRIMARY KEY(qso_date, time_on, band, mode, call));''')

            self.cursor.executescript(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании таблицы пользователя: ', Error)

    def select_user_id(self, telegram_id):
        users = self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return users.fetchone()

    def add_user_qso_data(self, user_call, data):
        self.cursor.executemany(f'INSERT OR IGNORE INTO {user_call} (call, qso_date, time_on, band, mode, gridsquare) VALUES (?, ?, ?, ?, ?, ?)', data)
        self.connection.commit()

    def search_qso_data(self, user_call, data):
        qsos = self.cursor.execute(f'SELECT call, gridsquare, qso_date, time_on, band, mode FROM {user_call} WHERE call LIKE ? OR gridsquare LIKE ?', ('%' + data + '%', '%' + data + '%'))
        return qsos.fetchall()


    def __del__(self):
        self.cursor.close()
        self.connection.close()