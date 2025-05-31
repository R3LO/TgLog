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
        query = f'''SELECT {user_call}.qso_date, {user_call}.call, {user_call}.band, {user_call}.mode,
            substr(IIF(t2.gridsquare not Null, t2.gridsquare, {user_call}.gridsquare), 1, 4) AS grid,
            IIF(t2.qsl_rcvd = 'Y', 'Y', 'N') AS qsl
            FROM {user_call}
            LEFT JOIN {lotw} AS t2 ON {user_call}.qso_date = t2.qso_date and {user_call}.call = t2.call and {user_call}.band = t2.band and {user_call}.mode = t2.mode
            WHERE {user_call}.call LIKE '%{data}%' OR grid LIKE '%{data}%'
            GROUP BY {user_call}.qso_date, {user_call}.call, {user_call}.band, {user_call}.mode, grid, qsl
            ORDER BY {user_call}.call, grid ASC'''
        qsos = self.cursor.execute(query)
        return qsos.fetchall()

    def get_total_qso_log(self, user_call):
        query_qsos = f'''
                    Select count(*) from {user_call};
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_full_log(self, user_call):
        query_qsos = f'''
                    Select * from {user_call};
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_total_qso_lotw(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    Select count(*) from {lotw};
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_total_uniq_log(self, user_call):
        query_qsos = f'''
                    SELECT call, qso_date, substr(time_on, 1, 4), band, mode from {user_call}
                    WHERE call IS NOT NULL and band = '13CM'
                    GROUP by call
                    ORDER BY call ASC;
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_total_uniq_lotw(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT call, qso_date, substr(time_on, 1, 4), band, mode from {lotw}
                    WHERE call IS NOT NULL and band = '13CM' and prop_mode = 'SAT' and sat_name = 'QO-100'
                    GROUP by call
                    ORDER BY call ASC;
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_stat_states(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT country, call, count(*) as QSPs from {lotw}
                    WHERE country IS NOT NULL and band = '13CM' and prop_mode = 'SAT' and sat_name = 'QO-100'
                    GROUP BY country
                    ORDER BY country ASC;
                    '''
        stat = self.cursor.execute(query_qsos)
        return stat.fetchall()


    def get_stat_loc(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT substr(gridsquare, 1, 4) as loc, call from {lotw}
                    WHERE loc IS NOT NULL and band = '13CM' and prop_mode = 'SAT' and sat_name = 'QO-100'
                    GROUP BY loc
                    ORDER BY loc ASC;
                    '''
        stat = self.cursor.execute(query_qsos)
        return stat.fetchall()

    def get_stat_cqz(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT cqz, call from {lotw}
                    WHERE cqz IS NOT NULL and band = '13CM' and prop_mode = 'SAT' and sat_name = 'QO-100'
                    GROUP BY cqz
                    ORDER BY cqz ASC;
                    '''
        stat = self.cursor.execute(query_qsos)
        return stat.fetchall()

    def get_stat_ituz(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT ituz, call from {lotw}
                    WHERE ituz IS NOT NULL and band = '13CM' and prop_mode = 'SAT' and sat_name = 'QO-100'
                    GROUP BY ituz
                    ORDER BY ituz ASC;
                    '''
        stat = self.cursor.execute(query_qsos)
        return stat.fetchall()


    def get_stat_bands(self, user_call):
        query_qsos = f'''
                    SELECT band, mode, count(*) as QSPs from {user_call}
                    GROUP BY band, mode
                    ORDER BY band, mode ASC;
                    '''
        stat = self.cursor.execute(query_qsos)
        return stat.fetchall()

    def delete_all_logs(self, user_call):
        lotw = user_call + '_lotw'
        query = f'''
                    DELETE FROM {user_call};
                    DELETE FROM {lotw};
                '''

        self.cursor.executescript(query)
        self.connection.commit()




    def __del__(self):
        self.cursor.close()
        self.connection.close()