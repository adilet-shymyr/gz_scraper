import pandas as pd
import os

# Путь к папке с файлами Excel
folder_path = 'C:/Users/manap.shymyr/PycharmProjects/goszakup/data'
output_file = 'C:/Users/manap.shymyr/PycharmProjects/goszakup/combined_datassss23555.xlsx'

# Список для хранения данных из каждого файла
data_list = []

# Проход по всем файлам в папке
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # Чтение файла Excel
            df = pd.read_excel(file_path, engine='openpyxl')  # Используйте 'openpyxl' для .xlsx файлов
            print(f'Чтение файла: {file_name}')

            # Убедитесь, что столбец БИН преобразован в строковый формат
            if 'БИН' in df.columns:
                df['БИН'] = df['БИН'].astype(str).str.zfill(12)  # Предположим, что БИН должен содержать 12 символов

            # Добавление данных из файла в список
            data_list.append(df)
        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")

# Объединение всех DataFrame в один
if data_list:
    combined_df = pd.concat(data_list, ignore_index=True)

    # Сохранение объединенного DataFrame в новый Excel файл
    combined_df.to_excel(output_file, index=False)
    print(f"Все файлы успешно объединены и сохранены в '{output_file}'")
else:
    print("Нет данных для объединения.")
