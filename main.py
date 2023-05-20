import os
import csv
from pprint import pprint
# Путь к папке, которую вы хотите открыть
folder_path = "Input"
if not os.path.isdir('Output'):
    os.mkdir('Output')
if not os.path.isdir('Input'):
    os.mkdir('Input')
if not os.listdir('Input'):
    input('Нет файлов в директории Input.\nДобавьте файлы для парсинга.\n\nНажмите Enter, чтобы выйти.')
    exit()

# Функция для проверки, является ли файл CSV-файлом
def is_csv_file(file_name):
    return file_name.endswith('.csv')


# Получаем список файлов в папке и фильтруем только CSV-файлы
file_list = [file_name for file_name in os.listdir(folder_path) if is_csv_file(file_name)]

# Выводим имена файлов в консоль
for index, file_name in enumerate(file_list):
    print(f"{index + 1}. {file_name}")

selected_file_index = None

# Цикл для предложения выбрать файл до ввода корректного номера
while selected_file_index is None or not 0 <= selected_file_index < len(file_list):
    # Просим пользователя выбрать номер файла
    selected_file_index = int(input("Выберите номер файла для чтения: ")) - 1

    if not 0 <= selected_file_index < len(file_list):
        print("Неверный номер файла. Попробуйте снова.")

# Открываем выбранный файл CSV и читаем его содержимое
selected_file = file_list[selected_file_index]
file_path = os.path.join(folder_path, selected_file)
with open(file_path, "r", encoding='utf-8') as file:
    csv_reader = csv.reader(file, delimiter=';')
    input_data = list(csv_reader)

# Отделяем первую строку в отдельную переменную и удаляем ее из изначального списка
header = ['Time', 'Frequency', 'Pressure']
input_data = input_data[1:]

# Обрабатываем оставшиеся строки
sensor_info = []
sensor_data = []
Date = input_data[0][0].split(' ')[0]  # Сохраняем лишние данные из первого элемента один раз
for index, row in enumerate(input_data):
    row[0] = row[0].split(' ')[-1]  # Оставляем только вторую часть
    row = [row[0]] + row[2:]  # Удаляем второй элемент (ноль) и оставляем остальные элементы

    if index % 48 < 24:
        sensor_info.append(row)
    else:
        sensor_data.append(row)

# Удаляем указанные элементы из списков sensor_info и sensor_data
sensor_info = [row[:1] + row[4:] for row in sensor_info]
sensor_data = [row[4:] for row in sensor_data]


dict_output = {}

flag = 0
while flag != 24:
    output = []
    for i in range(flag, len(sensor_data), 24):
        data = {'Time': sensor_info[i][0],
                'Frequency': float(sensor_info[i][1].replace(',', '.')),
                'Pressure': float(sensor_data[i][0].replace(',', '.'))}
        output.append(data)
    dict_output[f'Sensor{flag}'] = output
    flag = flag + 1
# pprint(dict_output)
# Выводим элементы списков sensor_info и sensor_data параллельно
# for info, data in zip(sensor_info, sensor_data):
#     print("Sensor Info:", info)
#     print("Sensor Data:", data)
#     print()

folder_name = input("Введите имя выходной папки:")
path = f'Output/{folder_name}_{Date}'
os.mkdir(path)
for key in dict_output:
    with open(f'{path}/{key}.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=header, delimiter=";")
        writer.writeheader()
        writer.writerows(dict_output[key])

input(f'Данные успешно выгружены в директорию: /{path}\nНажмите Enter, чтобы выйти.')