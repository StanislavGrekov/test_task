from connect import cursor, conn
from pprint import pprint
import datetime
import math


def checking_the_control_number(number):
    '''Функция на вход принимает СНИЛС. Eсли проверка контольного числа прошла успешно возвращает контрольное число. Eсли проверка не пройдена возращает строку, описывающую проблему'''

    value = int(number[0])
    print(type(value))

    last_three = int(number[8:11])

    if int(number[0]) == 0 and int(number[1]) == 0 and int(number[2]) == 1 and int(number[4]) == '0' and int(number[5]) == 0 and int(number[6]) == 1 and last_three <= 998: # Проверям, что СНИЛС больше 001-001-998
        return 'Невозможно сформировать контрольное число, т.к. страховой номер меньше 001-001-998!'

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

    print(f'Продукт {name_product} успешно добавлен клиенту .')


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







# 5 задание
def task_5():
    type_product = 'КРЕДИТ' # Устанавливаем тип продукта
    oper_date = '2015-10-01' # Устанавливаем дату проведения операций
    dt = 1 # Устанавливаем признак дебетования счета

    cursor.execute('''
        select pt.name,  avg(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt.name=%s AND r.oper_date  = %s AND r.dt = %s
        GROUP BY pt.name
         ''', (type_product, oper_date, dt))

    data = cursor.fetchall()
    conn.commit()
    for element in data:
        print(f'Тип продукта: {element[0]}, средняя сумма по операциям {int(element[1])}')



# 6 задача
def task_6():
    cursor.execute('''
        select c.name, r.oper_date, sum(r.sum)  from clients c
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        WHERE r.oper_date >= '2023-03-01' and r.oper_date <= '2023-03-31'
        group by c.name, r.oper_date 
         ''')
    data = cursor.fetchall()
    conn.commit()
    for element in data:
        print(f'Клиент: {element[0]}, дата: {element[1]}. Сумма операция на указанную дату: {element[2]}')

# 7 задача
def task_7():
    '''
    Не сталкивался с тем, чтобы данные в БД разъезжались, но мне кажется можно поступить как:
    -  найти r.acc_ref по операциям и сумму операций с  dt = 0 и отдельно c dt = 1 из таблицы records

        select r.acc_ref, sum(r.sum) from records r
        inner join accounts a on r.acc_ref = a.id
        where r.dt = 1
        group by r.acc_ref

        select r.acc_ref, sum(r.sum) from records r
        inner join accounts a on r.acc_ref = a.id
        where r.dt = 0
        group by r.acc_ref

    - далее найти a.id и a.saldo из таблички accounts

        select a.id, a.saldo  from accounts a

    - и, если я правильно понимаю что saldo это разница между суммами операций при  dt = 0 и dt = 1, нам нужно вписать значения
    a.id в r.acc_ref, где sum(r.sum, при dt = 0) - sum(r.sum при dt = 1) = a.saldo
       '''
    pass

# 8 задача
def task_8():
    '''Если я правильно понимаю, чтобы погасить кредит, надо чтобы общая сумма по операциям с dt=1 и dt=0
    равнялась нулю. Здесь я сначал нахожу клиента с продуктом Кредит и с пустой датой закрытия, а затем в цикле
     получаю сумму по операциям. Сумма равняется 2000, получается что клиент снова взял кредит.'''
    cursor.execute('''
        select c.name,  pt.name, r.sum, r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ'  AND p.close_date  is NULL
         ''')
    data = cursor.fetchall()
    pprint(data)
    conn.commit()
    count = 0
    for element in data:
        if element[3] == 1:
            count+=element[2]
        else:
            count -= element[2]
    print(f'Cумма кредита: {count}')


def task_9():
    '''
    Сначала я выполняю Select запросы к БД и нахожу клиентов у которых открыт продукт - Кредит,
    проверяю чтобы он не был закрыт и считаю сумму по операциям при dt = 0 и dt = 1. Потом я суммирую эти значения
    и определяю клиента, у которого сумма = 0. Этого клинета нахожу в БД и делаю ему в табличке products дату
    закрытия продукта.
    '''
    cursor.execute('''
        select c.name,  pt.name, SUM(r.sum), r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =1 AND p.close_date  is NULL
        GROUP by c.name,  pt.name,  r.dt
         ''')
    data = cursor.fetchall()
    dict_client_dt_1 = {}
    for element in data:
        dict_client_dt_1[element[0]] = [int(element[2])]



    cursor.execute('''
        select c.name,  pt.name, SUM(r.sum), r.dt  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =0 AND p.close_date  is NULL
        GROUP by c.name,  pt.name,  r.dt
         ''')
    data = cursor.fetchall()
    dict_client_dt_0 = {}
    for element in data:
        dict_client_dt_0[element[0]] = [-int(element[2])]


    conn.commit()

    rezult= {}

    for key_1, val_1 in  dict_client_dt_0.items():
        if key_1 in dict_client_dt_1:
            dict_client_dt_1[key_1].extend(val_1)
        else:
            dict_client_dt_1[key_1] = val_1
    rezult.update(dict_client_dt_1)

    date = datetime.datetime.now()
    close_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))

    for name,amount in rezult.items():
        if sum(amount) == 0:
            cursor.execute('''
                select p.id from products p
                inner join clients c on c.id =p.client_ref 
                where c.name = %s;''', (name,))

    id = cursor.fetchall()

    cursor.execute('''
        update products set close_date = %s WHERE id = %s;
        ''', (close_date, id[0][0]))
    print(f'Для клиента {name} установлена дата закрытия {close_date}')
    conn.commit()

def task_10():
    '''
    Сначала я нахожу клиентов, у которых были последнии операции 30 и больше дней назад.
     Затем в цикле я нахожу id продукта клиента и ставлю ему в дату закрытия сегодняшний день.
    '''
    cursor.execute('''
        select c.name, r.oper_date  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where r.oper_date  < CURRENT_DATE - 30
             ''')
    data = cursor.fetchall()
    conn.commit()

    date = datetime.datetime.now()
    close_date = (str(date.year) + '-' + str(date.month) + '-' + str(date.day))

    dict_client={}
    for element in data:
        dict_client[element[0]] = close_date

    for name, close_date in dict_client.items():
        cursor.execute('''
                select p.id from products p
                inner join clients c on c.id =p.client_ref 
                where c.name = %s;''', (name,))

        id = cursor.fetchall()

        cursor.execute('''
                 update products set close_date = %s WHERE id = %s;
                ''', (close_date, id[0][0]))
        print(f'Для клиента {name} установлена дата закрытия {close_date}')
    conn.commit()


def task_11():
    '''
    Добавляю в табличку accounts столбец sum_dogovor.
    Не понимаю, что такое "сумма максимальной дебетовой операции" поэтому я заполню поле sum_dogovor суммой дебетовых
    операций по продукту Кредит и суммой кредитовых операций по продукту Карта, Депозит
    '''

    # Запрос по продукту Кедит, дебетовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КРЕДИТ' AND r.dt =1 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s; 
            ''', (int(data[0][1]), 1)) # Здесь, конечно, сначала нужно вытаскивать product_ref через табличку products_type
    conn.commit()

    # Запрос по продукту Карта, кредитовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'КАРТА' AND r.dt =0 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s;
            ''', (int(data[0][1]), 3))
    conn.commit()

    # Запрос по продукту депозит, кредитовая операция
    cursor.execute('''
        select pt.name, SUM(r.sum)  from clients c
        inner join products p on c.id = p.client_ref
        inner join products_type pt on pt.id = p.product_type_id
        inner join accounts a on c.id = a.client_ref 
        inner join records r on a.id = r.acc_ref 
        where pt."name" = 'ДЕПОЗИТ' AND r.dt =0 
        GROUP by pt.name, r.dt
             ''')
    data = cursor.fetchall()

    pprint(int(data[0][1]))

    cursor.execute('''
            update accounts set sum_dogovor = %s WHERE product_ref = %s;
            ''', (int(data[0][1]), 2))
    conn.commit()


