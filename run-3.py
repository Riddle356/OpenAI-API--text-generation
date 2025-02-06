import pandas as pd
import re

def add_h2_to_description(products_file, h2_file, output_file):
    # Загружаем данные
    df_products = pd.read_csv(products_file, dtype=str)
    df_h2 = pd.read_csv(h2_file, dtype=str)
    
    # Объединяем таблицы по product_id и language_id
    df_merged = df_products.merge(df_h2[['product_id', 'language_id', 'h2']],
                                  on=['product_id', 'language_id'], how='left')
    
    # Добавляем h2 в начало description, если h2 есть
    df_merged['description'] = df_merged.apply(
        lambda row: "&lt;h2&gt;{}&lt;/h2&gt; {}".format(re.sub(r'^[^\wА-Яа-яЁё]+|[^\wА-Яа-яЁё]+$', '', row['h2'].strip()).replace("\"", "&quot;").replace("\'", "&quot;"), row['description']) if pd.notna(row['h2']) else row['description'],
        axis=1
    )
    
    # Убираем временное поле h2 перед сохранением
    df_merged.drop(columns=['h2'], inplace=True)
    
    # Сохраняем в новый файл
    df_merged.to_csv(output_file, index=False)
    print(f"Файл сохранен: {output_file}")

# Использование
add_h2_to_description("oc_product_description_for_editing.csv", "h2_results.csv", "updated_products_short.csv")


