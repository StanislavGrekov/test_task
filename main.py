from functions import checking_the_control_number, insert_clients, add_product, update_product

# Допустим, нам нужно занести в БД пользователя Сидорова Сидора со СНИЛС 208 921 461 66
first_name = 'Сидоров'
last_name = 'Сидор'
SNILS = '048 544 630 77'

# Проверяем контрольное число, если оно верно вносим клиента в БД. Cам СНИЛс в БД хранить не очень правильная идея, лучше хранить хэш снилса.
# Но для примера будем хранить в БД контрольное число.

# result = checking_the_control_number(SNILS)
#
# if type(result) == int:
#     control_number = result
#     insert_clients(control_number, first_name, last_name,)
# elif type(result) == str:
#     print(result)

# Теперь добавим продукт в таблицу products для клиента. Клиента найдем по контрольному числу СНИЛС.

# name_product = 'Депозит'
# value = '20000'
# SNILS = '048 544 630 77'
#
# result = checking_the_control_number(SNILS)
#
# if type(result) == int:
#     control_number = result
#     add_product(control_number, name_product, value,)
# elif type(result) == str:
#     print(result)

# Далее обновим таблицу products

value = '0'
SNILS = '048 544 630 77'

result = checking_the_control_number(SNILS)

if type(result) == int:
    control_number = result
    update_product(control_number, value)
elif type(result) == str:
    print(result)