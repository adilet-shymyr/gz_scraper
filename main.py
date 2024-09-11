import os
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

pd.set_option('display.max_rows', None)  
pd.set_option('display.max_columns', None)  
pd.set_option('display.width', None)  
pd.set_option('display.max_colwidth', None)  
year = '2021'
# BIN list
bins = [
    "030440003698", "990340005977", "780140000023", "051040005150", "990740002243",
    "971040001050", "020440003656", "970940001378", "940940000384", "100140011059",
    "000740001307", "980440001034", "940740000911", "171041003124", "050740004819",
    "150540000186", "020240002363", "230740013340", "210240019348", "210941010761",
    "120940001946", "210240033968", "960440000220", "900640000128", "960640000535",
    "140340016539", "231040023028"
]
# working path
data_folder = r"data"
# create path if not exists
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
# URL
url = 'https://v3bl.goszakup.gov.kz/ru/rep/rep/m001'

#setting for ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": data_folder,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    "profile.default_content_settings.popups": 0
})

# Initializing WebDriver using ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get(url)

# wait until Sign in is clickable
element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
)

downloaded_files = []

# loop for selenium
for bin_number in bins:
    # input year
    year_input = driver.find_element(By.ID, 'r1_rep_year')
    year_input.send_keys(year)

    # input bin
    bin_input = driver.find_element(By.CSS_SELECTOR, 'input[name="r1_cust_bin"]')
    bin_input.clear()
    bin_input.send_keys(bin_number)

    # press generate button
    generate_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-info')
    generate_button.click()

    # get data
    table_element = driver.find_element(By.ID, 'RepData')
    table_html = table_element.get_attribute('outerHTML')

    # process the data
    df = pd.read_html(table_html, header=3 )[0]  # Получаем первую таблицу
    df = df.drop(index=0)
    df = df.fillna('')
    df_filtered = df[['Способ закупки', 'Предметов договоров', 'Сумма, выделенная для закупки, (тенге)', 'Общий объем закупок, (тенге)']]
    df_filtered.insert(0, 'Год', year)
    df_filtered.insert(1, 'БИН', bin_number)

    # save processed data
    output_file = os.path.join(data_folder, f"{bin_number}_{year}.xlsx")
    df_filtered.to_excel(output_file, index=False, engine='openpyxl')
    print(f"Файл сохранен: {output_file}")

    driver.get(url)
    # captcha prevent
    time.sleep(3)

# end of first part
driver.quit()

print(f"Все файлы успешно сохранены в {data_folder}")


output_file = 'final_data.xlsx'

# list for storing data
data_list = []

# go through all the files in the folder
for file_name in os.listdir(data_folder):
    if file_name.endswith('.xls') or file_name.endswith('.xlsx'):
        file_path = os.path.join(data_folder, file_name)
        try:
            # reading Excel
            df = pd.read_excel(file_path, engine='openpyxl')
            print(f'Чтение файла: {file_name}')


            if 'БИН' in df.columns:
                df['БИН'] = df['БИН'].astype(str).str.zfill(12)  # bin contains 12 symbols

            # adding data from a file to a list
            data_list.append(df)
        except Exception as e:
            print(f"Ошибка при обработке файла {file_name}: {e}")

# Combining  all DataFrames
if data_list:
    combined_df = pd.concat(data_list, ignore_index=True)

    # Saving combined DataFrame in Excel файл
    combined_df.to_excel(output_file, index=False)
    print(f"Все файлы успешно объединены и сохранены в '{output_file}'")
else:
    print("Нет данных для объединения.")


