import requests
from bs4 import BeautifulSoup

# URL страницы с расписанием
url = "https://rasp.omgtu.ru/ruz/main"

# Отправляем запрос на получение страницы
response = requests.get(url)

# Используем библиотеку BeautifulSoup для парсинга HTML-кода страницы
soup = BeautifulSoup(response.content, 'html.parser')

# Находим таблицу расписания
schedule_table = soup.find('table', {'class': 'table table-bordered table-condensed table-hover'})

# Проверяем, была ли найдена таблица
if schedule_table is not None:
    # Извлекаем информацию из таблицы
    for row in schedule_table.find_all('tr'):
        # Находим заголовок ячейки
        header = row.find('th')
        if header:
            header_text = header.find('i').get('title')
        else:
            header_text = ""

        # Находим содержимое ячейки
        content = row.find('td')
        if content:
            content_text = content.text.strip()
        else:
            content_text = ""

        # Выводим результаты
        print(header_text + ":", content_text)
else:
    print("Таблица расписания не найдена на странице")


