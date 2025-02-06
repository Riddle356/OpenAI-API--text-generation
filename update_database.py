import csv

def proccess_csv(input_file):
    with open (input_file, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        results = []

        for row in reader:
            description = row.get("description")
            language_id = row.get("language_id")
            product_id = row.get("product_id")

            results.append({
                    "description": description,
                    "language_id": language_id,
                    "product_id": product_id,
                })
            
        # Запись результатов в выходной CSV
        create_sql(output_file, results)

def create_sql(output_file, results):
    with open(output_file, "w", encoding="utf-8", newline="") as file:
        
        for field in results:

            # Формирование запроса
            query = (
                f"UPDATE products "
                f"SET description = \"{field['description']}\" "
                f"WHERE product_id = {field['product_id']} AND language_id = {field['language_id']};\n"
            )
            
            if "h2" in field['description']:
                # Запись запроса в файл
                file.write(query)
            else:
                continue


input_file = "updated_products_short.csv"
output_file = "final_sql.sql"

proccess_csv(input_file)
