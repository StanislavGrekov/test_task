from connect import cursor, conn
import datetime
import math


def checking_the_control_number(number):
    '''Функция проверки контрольного числа. На вход принимает СНИЛС. Eсли проверка контольного числа прошла успешно возвращает
     контрольное число. Eсли проверка не пройдена возращает строку, описывающую проблему'''

    last_three = int(number[8:11])

    if int(number[0]) == 0 and int(number[1]) == 0 and int(number[2]) == 1 and int(number[4]) == 0 and int(number[5]) == 0 and int(number[6]) == 1 and last_three <= 998: # Проверям, что СНИЛС больше 001-001-998
        return 'Невозможно сформировать контрольное число, т.к. страховой номер меньше или равен 001-001-998!'

    else:
        сontrol_number_value = math.ceil((9*int(number[0])+8*int(number[1])+7*int(number[2])+  # Формирование контрольного числа
                                    6*int(number[4])+5*int(number[5])+4*int(number[6])+
                                    3*int(number[8])+2*int(number[9])+1*int(number[10]))/1.01)

        сontrol_number_value = (str(сontrol_number_value)[-2] + str(сontrol_number_value)[-1]) # Берем срез (нужно чтобы отбросить первое число, если сформированное контрольное число трехзначное)

        if сontrol_number_value == '01': # Обрабатываем частные случаи
            сontrol_number_value = '00'
        elif сontrol_number_value == '02':
            сontrol_number_value = '01'

        control_number = number[-2]+number[-1] # Берем контрольное число из number

        if сontrol_number_value == control_number: # Проводим сравнение сформированного контрольного числа и контрольного числа из СНИЛС
            return int(сontrol_number_value)
        else:
            return f'Проверка контрольного числа не пройдена {сontrol_number_value} != {control_number}'


def insert_clients(control_number, first_name, last_name):
    '''Функция для внесения клиента в таблицу clients'''
    cursor.execute('''
        insert into clients(contr_numb, first_name, last_name) 
        values (%s, %s, %s);
         ''', (control_number, first_name, last_name))

    conn.commit()
    print(f'Пользователь {first_name} успешно добвален в БД')


def add_product(contr_number, name_product, value):
    '''
    Функция добавления продукта клиенту в таблицу products.
    '''

    date = datetime.datetime.now()
    open_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))
    close_date = None

    cursor.execute('''
        SELECT id FROM clients
        WHERE contr_numb = %s;
    ''', (contr_number,))
    id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO products(client_ref, name_product, value, open_date, close_date)
        VALUES(%s, %s, %s, %s, %s);
    ''', (id,name_product, value, open_date, close_date))
    conn.commit()

    print(f'Продукт {name_product} успешно добавлен клиенту.')


def update_product(contr_number, value):
    '''
    Функция обновления продукта в таблице products.
    '''

    date = datetime.datetime.now()
    close_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))

    cursor.execute('''
        SELECT id FROM clients
        WHERE contr_numb = %s;
    ''', (contr_number,))
    id = cursor.fetchone()[0]

    cursor.execute('''
        UPDATE products SET value=%s, close_date=%s WHERE client_ref = %s;
    ''', (value, close_date, id))
    conn.commit()

    print(f'Продукт успешно обновлен.')


def select_clients(control_number):
    '''
    Функция, позволяющая найти продукт клиента).
    '''
    cursor.execute("""
                    SELECT c.last_name , c.first_name, p.name_product FROM clients c
                    INNER JOIN products p ON c.id = p.client_ref
                    WHERE c.contr_numb = %s;
                    """, (control_number,))
    answer = cursor.fetchone()

    conn.commit()

    print(f'У пользователя {answer[1]} {answer[0]} есть продукт {answer[2]}')




