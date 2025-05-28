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
                     prop_mode TEXT,
                     sat_name TEXT,
                     qsl_rcvd TEXT,
                     dxcc TEXT,
                     country TEXT,
                     cqz INTEGER,
                     ituz INTEGER,
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

    def add_user_lotw_data(self, user_call, data):
        self.cursor.executemany(f'INSERT OR IGNORE INTO {user_call} (call, band, mode, qso_date, time_on, prop_mode, sat_name, qsl_rcvd, dxcc, country, gridsquare, cqz, ituz) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.connection.commit()

    def search_qso_data(self, user_call, data):
        lotw = user_call + '_lotw'
        # qsos = self.cursor.execute(f'SELECT call, gridsquare, qso_date, time_on, band, mode FROM {user_call} WHERE call LIKE ? OR gridsquare LIKE ?', ('%' + data + '%', '%' + data + '%'))
        # query = f'''SELECT {user_call}.call, {user_call}.band, {user_call}.mode,
        #     substr(IIF(t2.gridsquare not Null, t2.gridsquare, {user_call}.gridsquare), 1, 4) AS grid,
        #     IIF(t2.qsl_rcvd = 'Y', 'Y', 'N') AS qsl, count(*)
        #     FROM {user_call}
        #     LEFT JOIN {lotw} AS t2 ON {user_call}.call = t2.call and {user_call}.band = t2.band and {user_call}.mode = t2.mode
        #     WHERE {user_call}.call LIKE '%{data}%' OR grid LIKE '%{data}%'
        #     GROUP BY {user_call}.call, {user_call}.band, {user_call}.mode, {user_call}.qso_date, grid,
        #     ORDER BY {user_call}.call, grid DESC'''
            # LIMIT 30;'''
        query = f'''SELECT {user_call}.call, {user_call}.band, {user_call}.mode,
            substr(IIF(t2.gridsquare not Null, t2.gridsquare, {user_call}.gridsquare), 1, 4) AS grid,
            IIF(t2.qsl_rcvd = 'Y', 'Y', 'N') AS qsl
            FROM {user_call}
            LEFT JOIN {lotw} AS t2 ON {user_call}.call = t2.call and {user_call}.band = t2.band and {user_call}.mode = t2.mode
            WHERE {user_call}.call LIKE '%{data}%' OR grid LIKE '%{data}%'
            GROUP BY {user_call}.call, {user_call}.band, {user_call}.mode, grid
            ORDER BY {user_call}.call, grid DESC'''
        qsos = self.cursor.execute(query)
        return qsos.fetchall()


    def __del__(self):
        self.cursor.close()
        self.connection.close()