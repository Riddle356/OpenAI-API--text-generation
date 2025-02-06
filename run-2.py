from openai import OpenAI
client = OpenAI(api_key="API_KEY")

import csv

def get_system_message(language_id, product_name):
    if language_id == "1":
        return f"Из данного текста {product_name} составь привлекательный заголовок H2 длиной около 60 символов для интернет-магазина, сохраняя ключевые слова."
    elif language_id == "2":
        return f"From the given text {product_name}, create an attractive H2 title of about 60 characters for an online store, preserving the keywords."


# Функция для генерации заголовков H2 через GPT
def generate_h2(product_name: str, language_id) -> str:
    """Генерация H2 через GPT"""
    prompt = (
        get_system_message(language_id, product_name)
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "assistant", "content": "You are a helpful assistant"},
                {"role": "user", "content": prompt}
            ],
            max_completion_tokens=100,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Ошибка при генерации H2 для '{product_name}': {e}")
        return ""

# Функция для обработки CSV-файла
def process_csv(input_file: str, output_file: str):
    """Обработка входного CSV и генерация H2"""
    results = []
    
    with open(input_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        iteration_count = 0  # Инициализация счетчика

        for row in reader:
            if iteration_count >= 1000:
                break  # Прерывание цикла после 10 итераций

            product_name = row.get("h2")
            language_id = row.get("id_language")
            if product_name:
                h2 = generate_h2(product_name, language_id)
                results.append({
                    "id_tovara": row.get("id_tovara"),
                    "language_id": language_id,
                    "name_tovara": product_name,
                    "h2": h2
                })
                iteration_count += 1  # Увеличение счетчика после каждой итерации

    # Запись результатов в выходной CSV
    write_csv(output_file, results)

# Функция для записи данных в CSV
def write_csv(output_file: str, data: list[dict]):
    """Запись данных в CSV"""
    if not data:
        return

    with open(output_file, "w", encoding="utf-8", newline="") as file:
        fieldnames = ["id_tovara", "language_id", "name_tovara", "h2"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Использование
input_csv = "long_h2_results.csv"  # Входной файл
output_csv = "h2_results_chatgpt.csv"  # Выходной файл
process_csv(input_csv, output_csv)
