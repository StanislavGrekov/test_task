from connect import cursor, conn


def create_table():
    '''
    Функция, создающая структуру БД
    '''
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
            id SERIAL primary key,
            contr_numb INTEGER NOT NULL,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20) NOT NULL
            );
                       
            CREATE TABLE IF NOT EXISTS products (
            id SERIAL primary key,
            client_ref INTEGER NOT NULL REFERENCES clients(id),
            name_product VARCHAR(100) NOT NULL,
            value NUMERIC(10,2),
            open_date DATE,
            close_date DATE
            );
                ''')
    conn.commit()
    print('Структура успешно создана.')


def drop():
    '''
    Функция, удаляющая структуру в БД
    '''
    cursor.execute('''
            DROP TABLE clients CASCADE;
            DROP TABLE products CASCADE;
        ''')
    conn.commit()
    print('Структура успешно удалена.')


if __name__ == '__main__':
    #drop() # Нужно закомментировать или раскомментировать необходимую функцию.
    create_table()
