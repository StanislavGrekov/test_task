from functions import checking_the_control_number, insert_clients, add_product

# Допустим, нам нужно занести в БД пользователя Сидорова Сидора со СНИЛС 208 921 461 66
first_name = 'Сидоров'
last_name = 'Сидор'
SNILS = '208 921 461 66'

# Проверяем контрольное число, если оно верно вносим клиента в БД. Cам СНИЛс в БД хранить не очень правильная идея, лучше хранить хэш снилса.
# Для примера будем хранить в БД контрольное число.

# result = checking_the_control_number(SNILS)
#
# if result[0] == True:
#     control_number = result[1]
#     insert_clients(int(control_number), first_name, last_name,)
# elif result[0] == False:
#     print("Контрольное число неверно!")

# Теперь добавим продукт в таблицу products для клиента. Клиента найдем по контрольному числу СНИЛС.
name_product = 'Депозит'
value = '20000'

result = checking_the_control_number(SNILS)

if result[0] == True:
    control_number = result[1]
    add_product(int(control_number), name_product, value,)
elif result[0] == False:
    print("Контрольное число неверно!")