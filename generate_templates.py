import csv
import random
import re

# Шаблоны для H2
TEMPLATES = {
    1: [
        "Купить {product_name} с доставкой по Минску",
        "Доставка {product_name} по всей Беларуси",
        "Закажите {product_name} с доставкой в Беларуси",
        "Быстрая доставка {product_name} в Минске",
        "Купить {product_name} в Минске",
        "Лучшие цены на {product_name} с доставкой по Минску",
        "Оформите заказ на {product_name} с доставкой Минск, Беларусь",
        "Доставить {product_name} по Минску и Беларуси",
        "Доставка {product_name} по Минску – удобно и быстро"
    ],  # Русский
    2: [
        "Buy {product_name} with delivery to Minsk",
        "Delivery of {product_name} all over Belarus",
        "Order {product_name} with delivery to Belarus",
        "Fast delivery of {product_name} in Minsk",
        "Buy {product_name} in Minsk",
        "Best prices for {product_name} with delivery to Minsk",
        "Place an order for {product_name} with delivery Minsk, Belarus",
        "Deliver {product_name} to Minsk and Belarus",
        "Delivery of {product_name} in Minsk - convenient and fast"
    ]   # Английский
}

# Файлы для записи результатов
OUTPUT_FILE = "h2_results.csv"
LONG_H2_FILE = "long_h2_results.csv"

    
# Функция для обработки текста
def process_match(match):
    return match.group(0)  # Оставляем текст в кавычках без изменений


def generate_h2(product_name: str, language_id: int) -> str | None:
    """Генерация H2 в зависимости от языка"""
    if language_id not in TEMPLATES:
        return None
    templates = TEMPLATES[language_id]

    # Регулярное выражение для поиска текста внутри кавычек
    pattern = r'("[^"]*"|&quot;[^&]*&quot;)'
    
    # Разбиваем текст, заменяя всё, что не в кавычках, на нижний регистр
    result = re.split(pattern, product_name)  # Разбиваем строку на части
    result = [part.lower() if not re.match(pattern, part) else part for part in result]  
    
    return random.choice(templates).format(product_name=''.join(result))


def process_csv(input_file: str):
    """Обработка CSV-файла"""
    results = []
    long_h2_results = []

    # Чтение исходного файла
    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            product_id = row.get("id_tovara")
            language_id = int(row.get("id_language", 0))
            product_name = row.get("name_tovara", "").strip()
            product_category = row.get("category_tovara", "")

            if not product_name:  # Проверка на пустое название товара
                h2 = None
            else:
                # Генерация H2
                h2 = generate_h2(product_name, language_id)

            # Проверка длины H2
            if h2 and len(h2) > 50:
                long_h2_results.append({
                    "id_tovara": product_id,
                    "id_language": language_id,
                    "name_tovara": product_name,
                    "category_tovara": product_category,
                    "h2": h2,
                })
            else:
                results.append({
                    "id_tovara": product_id,
                    "id_language": language_id,
                    "name_tovara": product_name,
                    "category_tovara": product_category,
                    "h2": h2,
                })

    # Запись результатов
    write_csv(OUTPUT_FILE, results)
    write_csv(LONG_H2_FILE, long_h2_results)


def write_csv(output_file: str, data: list[dict]):
    """Запись данных в CSV"""
    if not data:
        return

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["id_tovara", "id_language", "name_tovara", "category_tovara", "h2"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Использование
input_csv = "your_csv.csv"  # Замените на путь к вашему CSV-файлу
process_csv(input_csv)
