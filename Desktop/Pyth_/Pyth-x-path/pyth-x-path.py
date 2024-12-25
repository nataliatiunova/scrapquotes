# HTTP-запрос с использованием requests
import requests
from lxml import html
import csv

# URL веб-страницы с таблицей
URL = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

# Заголовки запроса с User-Agent для имитации браузера
headers = {
    "User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}

# Имя файла для сохранения данных
csv_data_file = "countries_table_data.csv"

try:
    # GET-запрос
    response = requests.get(URL, headers=headers)
    response.raise_for_status()
    if response.status_code == 200:
        print("Запрос выполнен успешно")
    
    # Парсинг содержимого HTML с помощью lxml
    tree = html.fromstring(response.content)
    
    # Нахождение строк таблицы с помощью XPath
    rows = tree.xpath('//*[@id="mw-content-text"]/div[1]/table[1]/tbody/tr')
    if not rows:
        raise ValueError("Таблица не найдена на странице.")
    print(f"Найдено строк: {len(rows)}")
    
    # Извлечение данных из строк таблицы
    data_countries_population = []
    for row in rows:
        try:
            # Извлечение ячеек строки
            cells = row.xpath('td')
            if len(cells) >= 2:  # Проверяем, что строка содержит хотя бы 2 ячейки
                # Извлечение названия страны
                country_elements = cells[1].xpath('.//a[not(contains(@href, "note"))]/text() | .//text()')
                if not country_elements:
                    print("Пропускаем строку из-за отсутствия названия страны.")
                    continue
                country = ''.join(country_elements).strip()
                
                # Извлечение данных о населении
                population_elements = cells[2].xpath('.//text()')
                if not population_elements:
                    print("Пропускаем строку из-за отсутствия данных о населении.")
                    continue
                population = ''.join(population_elements).strip().replace(',', '')

                # Пропускаем строки с дефисами
                if country == "—" or population == "—":
                    print("Пропускаем строку с дефисом вместо данных.")
                    continue

                # Добавляем данные в список
                data_countries_population.append([country, population])
        except Exception as e:
            print(f"Ошибка обработки строки: {e}")
    
    # Сохранение данных в CSV-файл
    with open(csv_data_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Country", "Population"])  # Заголовок
        writer.writerows(data_countries_population)
        print(f"Данные успешно сохранены в {csv_data_file}")
    
except requests.exceptions.RequestException as e:
    print(f"Ошибка при выполнении HTTP-запроса: {e}")
except ValueError as e:
    print(f"Ошибка обработки данных: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")
