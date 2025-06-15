import sqlite3

def rating():
    # Подключение к базе данных
    conn = sqlite3.connect('tgbot_QO100.db')
    # Создание объекта курсора
    cursor = conn.cursor()

    dict_ru = {}
    dict_states = {}
    dict_loc = {}
    dict_unique = {}
    # Выполнение запроса на получение списка всех таблиц в базе данных
    cursor.execute("""SELECT name FROM sqlite_master WHERE type='table'
                        and name like '%_lotw'
                        order by name;""")
    # Получение результатов запроса
    tables = cursor.fetchall()
    for table in tables:
        # -----------------------------------
        query_states = f'''
            SELECT count(*) FROM (
               SELECT country FROM {table[0]}
                GROUP BY country
                HAVING country IS NOT NULL
            )
            ;
            '''
        states = cursor.execute(query_states)
        res_states = states.fetchall()
        if res_states[0][0]:
            table_states = table[0].replace('_lotw', '')
            dict_states[table_states] = res_states[0][0]
        dict_states_sorted = sorted(dict_states.items(), key=lambda item: item[1], reverse=True)
        # -----------------------------------
        query_ru = f'''
            select count(*) as ru from (
                    SELECT state from {table[0]}
                    WHERE country in ('EUROPEAN RUSSIA', 'ASIATIC RUSSIA', 'KALININGRAD')
                    GROUP BY state
                    HAVING state <> ''
                    ORDER BY state ASC
                    )
            '''
        rus = cursor.execute(query_ru)
        res_rus = rus.fetchall()
        if res_rus[0][0]:
            table_rus = table[0].replace('_lotw', '')
            dict_ru[table_rus] = res_rus[0][0]
        dict_ru_sorted = sorted(dict_ru.items(), key=lambda item: item[1], reverse=True)
        # -----------------------------------
        query_loc = f'''
                select count(*) from (
                    SELECT  substr(gridsquare, 1, 4) as loc from {table[0]}
                    group by loc
                    HAVING loc IS NOT NULL
                );
            '''
        loc = cursor.execute(query_loc)
        res_loc = loc.fetchall()
        if res_loc[0][0]:
            table_loc = table[0].replace('_lotw', '')
            dict_loc[table_loc] = res_loc[0][0]
        dict_loc_sorted = sorted(dict_loc.items(), key=lambda item: item[1], reverse=True)
        # -----------------------------------
        query_unique = f'''
                select count(*) from (
                    SELECT  call from {table[0]}
                    group by call
                );
            '''
        unique = cursor.execute(query_unique)
        res_unique = unique.fetchall()
        if res_unique[0][0]:
            table_unique = table[0].replace('_lotw', '')
            dict_unique[table_unique] = res_unique[0][0]
        dict_unique_sorted = sorted(dict_unique.items(), key=lambda item: item[1], reverse=True)


    conn.close()
    return [dict_ru_sorted, dict_states_sorted, dict_loc_sorted, dict_unique_sorted]