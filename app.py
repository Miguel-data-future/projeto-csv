# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import csv
import sqlite3
from pydantic import BaseModel, ValidationError

# FUNÇÕES PARA LISTAR OS TÍTULOS DISPONÍVEIS E POR TIPO

def listar_titulos(lista):
    conexao = sqlite3.connect('netflix.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT title FROM netflix")
    titulos = cursor.fetchall()
    conexao.close()
    return [titulo[0] for titulo in titulos]

def listar_titulos_por_tipo(tipo):
    conexao = sqlite3.connect('netflix.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT title FROM netflix WHERE type = ?", (tipo,))
    titulos = cursor.fetchall()
    conexao.close()
    return [titulo[0] for titulo in titulos]

def listar_titulos_com_ano_movie():
    conexao = sqlite3.connect('netflix.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT title, release_year FROM netflix where type = 'Movie'")
    titulos = cursor.fetchall()
    conexao.close()
    return titulos


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
sucesso = True
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
            sucesso = False

if sucesso:
    print("Todos os registros foram validados e inseridos com sucesso!")

else:
    print(" Processo concluído, mas alguns registros apresentaram erros de validação..")

create_database.commit()
create_database.close()

#receber a lista de todos os itens 
pesquisa = input(
    "Para listar os títulos disponíveis, digite 'Listar'. Para ignorar a pesquisa, digite 'Ignore': ")

if pesquisa == "Listar" or pesquisa == "listar":
    for titulo in listar_titulos():
        print(titulo)

elif pesquisa == 'ignore' or pesquisa == 'Ignore':
    print("Pesquisa ignorada.")

else:
    print("Título não encontrado.")

#receber a lista de itens por tipo (filme ou série)
input_tipo = input(
    "Digite o tipo de título que deseja listar (Filme ou Série): ")

if input_tipo == "Filme" or input_tipo == "filme":
    for titulo in listar_titulos_por_tipo("Movie"):
        print(titulo)
elif input_tipo == "Série" or input_tipo == "série":
    for titulo in listar_titulos_por_tipo("TV Show"):
        print(titulo)
else:
    print("Tipo de título não encontrado.")

    if input_tipo == "Filme" or input_tipo == "filme":
          
          input_ano = input("Digite 'Ano' para listar os títulos com ano de lançamento: ")

if input_ano.lower() == "ano":
    for titulo, ano in listar_titulos_com_ano_movie():
        print(f"{titulo} - {ano}")
else:
    print("Entrada inválida.")



  



#receber ano de lançamento


 

