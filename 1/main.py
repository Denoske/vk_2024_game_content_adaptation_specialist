import os
import requests
import winreg as reg
import subprocess
import sys

# Конфигурация
url = "https://drive.usercontent.google.com/open?id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH&authuser=0" 
download_directory = "C:\\Path\\To\\Game\\Directory"  # Путь к директории игры
file_name = "settings.reg"  # Имя скачиваемого файла
file_path = os.path.join(download_directory, file_name)

# Шаг 1: Скачивание файла
def download_file(url, dest):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка статуса ответа
        with open(dest, 'wb') as file:
            file.write(response.content)
        print(f"Файл загружен: {dest}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка загрузки: {e}")
        sys.exit(1)

# Шаг 2: Внесение значений в реестр
def modify_registry(path, key, value):
    try:
        # Открываем ключ реестра
        with reg.OpenKey(reg.HKEY_CURRENT_USER, path, 0, reg.KEY_SET_VALUE) as registry_key:
            reg.SetValueEx(registry_key, key, 0, reg.REG_SZ, value)
            print(f"Значение добавлено в реестр: {key} = {value}")
    except WindowsError as e:
        print(f"Ошибка при изменении реестра: {e}")
        sys.exit(1)

# Шаг 3: Запуск Steam или игры
def launch_steam_or_game(game_path):
    try:
        subprocess.Popen(game_path, shell=True)
        print("Игра или Steam запущен.")
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        sys.exit(1)

# Основная логика
if __name__ == "__main__":
    # Скачиваем файл
    download_file(url, file_path)

    # Обработка файла (например, чтение значений)
    try:
        with open(file_path, 'r') as file:
            for line in file:
                key, value = line.strip().split('=')  # Предполагается формат ключ=значение
                modify_registry("SOFTWARE\\YourSoftware", key, value)  # Замените на актуальный путь реестра

    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        sys.exit(1)

    # Запуск Steam
    steam_path = r"C:\Program Files (x86)\Steam\steam.exe"  # Путь к Steam
    launch_steam_or_game(steam_path)
