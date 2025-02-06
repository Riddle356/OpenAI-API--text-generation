# 📝 H2 Headings Generator & SQL Updater  

## 📌 Overview  
This Python-based program automates the creation, refinement, and database updating of **H2 headings** for products. It leverages the **OpenAI API** to generate headings and processes them before committing updates to a database via **SQL UPDATE statements**.  

## 🏗️ Program Structure  
The project consists of four key components:  

1. **`generate_templates.py`** – Creates initial H2 headings using predefined templates and product names.  
2. **`generate_openai.py`** – Uses the OpenAI API to refine and generate enhanced H2 headings based on the template-generated data.  
3. **`clean_responses.py`** – Processes and cleans OpenAI-generated responses by removing unnecessary symbols or formatting issues.  
4. **`update_database.py`** – Constructs `UPDATE` SQL queries and commits the new H2 headings to the database.  

## ⚙️ Installation & Setup  
1. Clone the repository:  
   ```bash
   git clone https://github.com/Riddle356/OpenAI-API-text-generation.git
   cd h2-headings-generator
