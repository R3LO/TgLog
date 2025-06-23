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
                     'user_call TEXT UNIQUE,'
                     'user_name TEXT,'
                     'telegram_id TEXT);'

                     'CREATE TABLE IF NOT EXISTS w100c('
                     'call TEXT UNIQUE PRIMARY KEY,'
                     'number INTEGER NOT NULL DEFAULT 0);'

                     'CREATE TABLE IF NOT EXISTS w100l('
                     'call TEXT UNIQUE PRIMARY KEY,'
                     'number INTEGER NOT NULL DEFAULT 0);'

                    'CREATE TABLE IF NOT EXISTS w1000b('
                     'call TEXT UNIQUE PRIMARY KEY,'
                     'number INTEGER NOT NULL DEFAULT 0);'

                     'CREATE TABLE IF NOT EXISTS w1000u('
                     'call TEXT UNIQUE PRIMARY KEY,'
                     'number INTEGER NOT NULL DEFAULT 0);'

                     'CREATE TABLE IF NOT EXISTS w25r('
                     'call TEXT UNIQUE PRIMARY KEY,'
                     'number INTEGER NOT NULL DEFAULT 0);')

            self.cursor.executescript(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании БД: ', Error)

    def check_call_diplomas(self, user, table):
        query = f'''
                SELECT number FROM {table}
                WHERE call = '{user}'
                LIMIT 1
                ;
                '''
        numbers = self.cursor.execute(query)
        res = numbers.fetchone()
        if res is None:
            return (0, )
        else:
            return res


    def get_last_number_diplomas(self, table):
        query = f'''
                    SELECT * FROM {table}
                    ORDER BY number DESC
                    LIMIT 1;
                    '''
        numbers = self.cursor.execute(query)
        last_number = numbers.fetchone()
        if last_number is None:
            return (0, 0)
        else:
            return last_number

    def add_call_diplomas(self, user, table, number):
        self.cursor.execute(f'INSERT OR REPLACE INTO {table} (call, number) VALUES (?, ?)', (user, number))
        self.connection.commit()



    def add_user(self, user_call, user_name, telegram_id) -> None:
        '''
        Добавление пользователя в базу user
        - позывной
        - имя
        - Telegram ID

        '''
        self.cursor.execute(f'INSERT INTO users (user_call,user_name, telegram_id) VALUES (?, ?, ?)', (user_call,user_name, telegram_id))
        self.connection.commit()

    def edit_user(self, user_call, user_name) -> None:
        self.cursor.execute(f"UPDATE users SET user_name = '{user_name}' WHERE user_call = '{user_call}'")
        self.connection.commit()


    def add_table_user(self, user_call) -> None:
        '''
        Создание таблиц пользователя
        - основной лог
        - LoTW лог

        '''

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
                     rst_rcvd TEXT,
                     rst_sent TEXT,
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
                     state TEXT,
                     cqz INTEGER,
                     ituz INTEGER,
                     operator TEXT,
                     paper_qsl TEXT DEFAULT N,
                     PRIMARY KEY(qso_date, time_on, band, mode, call));''')

            self.cursor.executescript(query)
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании таблицы пользователя: ', Error)

    def select_user_id(self, telegram_id):
        users = self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return users.fetchone()

    def add_user_qso_data(self, user_call, data):
        '''
        Добавить данные ADIF в БД основной лог

        '''
        self.cursor.executemany(f'INSERT OR REPLACE INTO {user_call} (call, qso_date, time_on, band, mode, gridsquare, operator, rst_rcvd, rst_sent) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.connection.commit()


    def add_user_lotw_data(self, user_call, data):

        '''
        Добавить данные LoTW ADIF в БД

        '''
        self.cursor.executemany(f'INSERT OR REPLACE INTO {user_call} (call, band, mode, qso_date, time_on, prop_mode, sat_name, qsl_rcvd, dxcc, country, gridsquare, state, cqz, ituz, operator) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        self.connection.commit()

    def search_qso_data(self, user_call, data):
        lotw = user_call + '_lotw'
        query = f'''
            SELECT date({user_call}.qso_date), {user_call}.call, {user_call}.band, {user_call}.mode,
            substr(
                IIF(t2.gridsquare not Null, t2.gridsquare,
                    IIF(t2.gridsquare = '', t2.gridsquare,
                        IIF(t2.gridsquare = 'None', t2.gridsquare, {user_call}.gridsquare)
                    ))
                , 1, 4) AS grid,
            IIF(t2.qsl_rcvd = 'Y', 'Y', 'N') AS qsl
            FROM {user_call}
            LEFT JOIN {lotw} AS t2 ON
                    date({user_call}.qso_date) = date(t2.qso_date)
                    and {user_call}.call = t2.call
                    and {user_call}.band = t2.band
                    and {user_call}.mode = t2.mode
                    and time({user_call}.time_on) between time(t2.time_on, '-30 minutes') and time(t2.time_on, '+30 minutes')
            WHERE {user_call}.call LIKE '%{data}%' OR grid LIKE '%{data}%'
            GROUP BY date({user_call}.qso_date), {user_call}.call, {user_call}.band, {user_call}.mode, grid, qsl
            ORDER BY date({user_call}.qso_date) DESC
            LIMIT 80'''
        qsos = self.cursor.execute(query)
        return qsos.fetchall()

    def get_total_qso_log(self, user_call):
        query_qsos = f'''
                    Select count(*) from {user_call};
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_full_log(self, user_call):
        '''
        Забрать весь лог
        '''
        query_qsos = f'''
                    Select * from {user_call}
                    ORDER BY qso_date ASC;
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

    def get_cosmos_uniq_log(self, user_call):
        query_qsos = f'''
                    SELECT IIF({user_call}.gridsquare IS NULL, t2.gridsquare,
                                    IIF({user_call}.gridsquare = '', t2.gridsquare,
                                        IIF({user_call}.gridsquare = 'None', t2.gridsquare, {user_call}.gridsquare)
                                    )) as grid
                    , {user_call}.qso_date, {user_call}.band, {user_call}.time_on, {user_call}.mode, {user_call}.call, {user_call}.rst_sent, {user_call}.rst_rcvd
                    FROM {user_call}
                    LEFT JOIN {user_call+'_lotw'} AS t2
                    ON date({user_call}.qso_date) = date(t2.qso_date)
                    and {user_call}.call = t2.call and
                    {user_call}.band = t2.band and
                    {user_call}.time_on = t2.mode and
                    time({user_call}.time_on) between time(t2.time_on) and time(t2.time_on)
                    WHERE {user_call}.call IS NOT NULL and {user_call}.band = '13CM' -- and grid IS NOT NULL
                    -- WHERE grid IS NOT NULL AND grid <> '' AND {user_call}.call IS NOT NULL and {user_call}.band = '13CM'
                    GROUP by {user_call}.call
                    -- HAVING grid IS NOT NULL
                    -- HAVING grid IS NULL
                    ORDER BY {user_call}.qso_date ASC
                    ;
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_total_uniq_log(self, user_call):
        query_qsos = f'''
                    SELECT call, qso_date, substr(time_on, 1, 5), band, mode from {user_call}
                    WHERE call IS NOT NULL and band = '13CM'
                    GROUP by call
                    ORDER BY call ASC;
                    '''
        qsos = self.cursor.execute(query_qsos)
        return qsos.fetchall()

    def get_total_uniq_lotw(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT call, qso_date, substr(time_on, 1, 5), band, mode from {lotw}
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

    def get_stat_ru(self, user_call):
        lotw = user_call + '_lotw'
        query_qsos = f'''
                    SELECT rr.description, call from {lotw}
                    LEFT JOIN rda_reg rr ON {lotw}.state = rr.rda
                    WHERE country in ('EUROPEAN RUSSIA', 'ASIATIC RUSSIA', 'KALININGRAD')
                    GROUP BY state
                    HAVING state <> ''
                    ORDER BY description ASC;
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
                    DELETE FROM {lotw} WHERE paper_qsl = 'N';
                '''
        self.cursor.executescript(query)
        self.connection.commit()

    def delete_main_log(self, user_call):
        query = f'''
                    DELETE FROM {user_call};
                '''
        self.cursor.executescript(query)
        self.connection.commit()

    def delete_lotw_log(self, user_call):
        lotw = user_call + '_lotw'
        query = f'''
                    DELETE FROM {lotw} WHERE paper_qsl = 'N';
                '''
        self.cursor.executescript(query)
        self.connection.commit()




    def __del__(self):
        self.cursor.close()
        self.connection.close()