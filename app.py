import csv
import sqlite3

create_database = sqlite3.connect('netflix.db')
cursor = create_database.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS netflix (
    show_id TEXT PRIMARY KEY,
    type TEXT,
    title TEXT,
    director TEXT,
    cast TEXT,
    country TEXT,
    date_added TEXT,
    release_year INTEGER,
    rating TEXT,
    duration TEXT,
    listed_in TEXT,
    description TEXT
)
''')

with open('netflix_titles.csv', 'r', encoding='utf-8') as arquivo:
    arquivo_csv = csv.reader(arquivo, delimiter=',')
    next(arquivo_csv)  # Pula o cabeçalho do CSV

    for row in arquivo_csv:
         cursor.execute('''
              INSERT OR REPLACE INTO netflix (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
                VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', row)

create_database.commit()
create_database.close()




   


