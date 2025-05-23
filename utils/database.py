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
        
    def select_user_id(self, telegram_id):
        users = self.cursor.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        return users.fetchone()
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()