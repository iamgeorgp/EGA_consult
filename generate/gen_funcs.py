import random
import os
import pandas as pd
def generate_phone_number(size):
    phone_numbers = []
    for i in range(size):
        area_code = random.randint(200, 999)  # Генерация трехзначного кода области
        exchange_code = random.randint(200, 999)  # Генерация трехзначного кода обмена
        line_number = random.randint(1000, 9999)  # Генерация четырехзначного номера линии

        # Форматирование номера в стандартный формат США
        phone_number = f"({area_code}) {exchange_code}-{line_number}"
        phone_numbers.append(phone_number)
    return phone_numbers


def generate_full_name(size):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(os.path.dirname(script_directory), "data")
    # Чтение строк из файла и сохранение их в массив
    with open(data_directory + '\\' + 'surname.txt', 'r', encoding='utf-8') as file:
        surnames_array = file.readlines()
    with open(data_directory + '\\' + 'name.txt', 'r', encoding='utf-8') as file:
        names_array = file.readlines()
    print('ready')
    names_array_len = len(names_array)
    surnames_array_len = len(surnames_array)
    full_names=[]
    for i in range(size):
        name = names_array[random.randint(0, names_array_len)].strip()
        surname = surnames_array[random.randint(0, surnames_array_len)].strip()
        full_names.append(name + ' ' + surname)
    return full_names


def generate_company(size):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    data_directory = os.path.join(os.path.dirname(script_directory), "data")
    df_company = pd.read_csv(data_directory+'\AllCompanyNames.csv', encoding='cp1251')
    company_names = []
    df_n_rows = df_company.shape[0]
    for i in range(size):
        company_names.append(df_company.iloc[random.randint(0, df_n_rows), 0])
    return company_names


print(generate_phone_number(5)
)
