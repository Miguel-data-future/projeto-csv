# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import csv
import sqlite3
from pydantic import BaseModel, ValidationError


# VALIDAÇÃO DE DADOS COM PYDANTIC
class Netflix(BaseModel):
    show_id: str
    type: str
    title: str
    director: str | None
    cast: str | None
    country: str | None
    date_added: str | None
    release_year: int
    rating: str | None
    duration: str | None
    listed_in: str | None
    description: str | None


# CRIAÇÃO DO BANCO DE DADOS
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

# INSERÇÃO DOS DADOS DO CSV COM VALIDAÇÃO
with open('netflix_titles.csv', 'r', encoding='utf-8-sig') as arquivo:
    arquivo_csv = csv.DictReader(arquivo)
    for row in arquivo_csv:

        try:  # TENTA VALIDAR CADA REGISTRO DO CSV USANDO O MODELO Pydantic. SE HOUVER UM ERRO DE VALIDAÇÃO, ELE SERÁ CAPTURADO E IMPRESSO, MAS O PROCESSO CONTINUARÁ PARA OS DEMAIS REGISTROS.
            registro = Netflix(**row)
            cursor.execute('''
                INSERT OR REPLACE INTO netflix 
                (show_id, type, title, director, cast, country, date_added, release_year, rating, duration, listed_in, description)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
            ''', tuple(row.values()))

        except ValidationError as e:
            # IMPRIME SE HOUVER ERRO DE VALIDAÇÃO.
            print(f"Erro de validação para o registro {row['show_id']}: {e}")


create_database.commit()
create_database.close()
