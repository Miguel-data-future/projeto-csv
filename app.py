# IMPORTANDO AS BIBLIOTECAS NECESSÁRIAS
import csv
import sqlite3
from pydantic import BaseModel, ValidationError


def listar_titulos(): # FUNÇÃO PARA LISTAR OS TÍTULOS DISPONÍVEIS 
    conexao = sqlite3.connect('netflix.db')
    cursor = conexao.cursor()
    cursor.execute("SELECT title FROM netflix")
    titulos = cursor.fetchall()
    conexao.close()
    return [titulo[0] for titulo in titulos]


    return [titulo[0] for titulo in titulos]


def listar_titulos_com_info(tipo):  # FUNÇÕES PARA LISTAR OS TÍTULOS COM INFORMAÇÕES
    conexao = sqlite3.connect('netflix.db')
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT title, release_year, country FROM netflix WHERE type = ?", (tipo,))
    titulos = cursor.fetchall()
    conexao.close()
    return [(titulo[0], titulo[1], titulo[2]) for titulo in titulos]


def quant_titulos(): # FUNÇÃO PARA LISTAR A QUANTIDADE DE TÍTULOS DISPONÍVEIS POR TIPO (FILME)
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM netflix WHERE type = 'Movie'")
    qtd_filmes = cursor.fetchone()[0]
    return qtd_filmes


def quant_titulos(): # FUNÇÃO PARA LISTAR A QUANTIDADE DE TÍTULOS DISPONÍVEIS POR TIPO (SÉRIE)
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM netflix WHERE type = 'TV Show'")
    qtd_series = cursor.fetchone()[0]
    return qtd_series


def listar_paises_unicos(): #FUNÇAO PARA LISTAR TODOS OS FILMES DE CADA PAÍS DISPONÍVEIS
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT country FROM netflix WHERE country != '' AND country != 'Desconhecido'")
    paises_raw = cursor.fetchall()
    conexao.close()

    paises_unicos = set()
    for linha in paises_raw:
        if linha[0]:
            for pais in linha[0].split(","):
                paises_unicos.add(pais.strip())
    return sorted(paises_unicos)


def listar_filmes_por_pais(pais): 
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT title 
        FROM netflix 
        WHERE type = 'Movie' AND country LIKE ?
    """, (f"%{pais}%",))
    filmes = cursor.fetchall()
    conexao.close()
    return [filme[0] for filme in filmes]


def listar_anos_unicos(): #LISTAR FILMES DE CADA ANO DISPONÍVEIS
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT DISTINCT release_year FROM netflix WHERE release_year IS NOT NULL")
    anos_raw = cursor.fetchall()
    conexao.close()

   
    anos_unicos = sorted({ano[0] for ano in anos_raw})
    return anos_unicos

def listar_filmes_por_ano(ano):
    conexao = sqlite3.connect("netflix.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT title 
        FROM netflix 
        WHERE type = 'Movie' AND release_year = ?
    """, (ano,))
    filmes = cursor.fetchall()
    conexao.close()
    return [filme[0] for filme in filmes]


class Netflix(BaseModel): # VALIDAÇÃO DE DADOS COM PYDANTIC
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


create_database = sqlite3.connect('netflix.db')# CRIAÇÃO DO BANCO DE DADOS
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


sucesso = True # INSERÇÃO DOS DADOS DO CSV COM VALIDAÇÃO

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


conexao = sqlite3.connect("netflix.db")  # abre uma nova conexão
cursor = conexao.cursor()
colunas = ['show_id', 'type', 'title', 'director', 'cast', 'country', 'date_added',
           'release_year', 'rating', 'duration', 'listed_in', 'description']

for coluna in colunas:
    cursor.execute(
        f'UPDATE netflix SET "{coluna}" = "Desconhecido" WHERE "{coluna}" IS NULL OR "{coluna}" = ""')

conexao.commit()


conexao.close()

while True: 
    opcoes = input("Escolha uma opção: \n \n"
                "1 - Listar todos os títulos disponíveis\n \n"
                "2 - Listar títulos por tipo (filme ou série)\n \n"
                "3 - Quantidade de títulos\n \n"
                "4 - Listar filmes de cada país\n \n"
                "5 - Listar filmes de cada ano\n \n")


    # (1) RECEBER A OPÇÃO DO USUÁRIO PARA LISTAR OS TÍTULOS DISPONÍVEIS

    if opcoes == "1":
        for titulo in listar_titulos():
            print(titulo)


    # (2) RECEBER OS ITENS DA LITA POR TIPO DE TÍTULO (FILME OU SÉRIE) E IMPRIMIR O RESULTADO

    elif opcoes.lower() == "2":
        print("Digite o tipo de título que deseja listar:\n"
            "3 - filme\n"
            "4 - série")
        input_tipo = input()

        if input_tipo.lower() == "3":
            for titulo, ano, pais in listar_titulos_com_info("Movie"):
                print(f"{titulo} - {ano} - {pais}")

        elif input_tipo.lower() == "4":
            for titulo, ano, pais in listar_titulos_com_info("TV Show"):
                print(f"{titulo} - {ano} - {pais}")

        else:
            print("Tipo de título não encontrado.")


    #(3) RECEBER A OPÇÃO DO USUÁRIO PARA LISTAR A QUANTIDADE DE TÍTULOS DISPONÍVEIS

    if opcoes == "3":
        escolha_quantidade = input("1 - filmes\n" "2 - séries\n \n")
        if escolha_quantidade == "1":
            print(f"Quantidade de filmes disponíveis: {quant_titulos()}")

        elif escolha_quantidade == "2":
            print(f"Quantidade de séries disponíveis: {quant_titulos()}")

        else:
            print("Opção inválida.")

    # (4)RECEBER OPÇÕES DOS FILMES DE CADA PAÍS

    if opcoes == "4":

        paises = listar_paises_unicos()

        print("Escolha um país da lista:")
        for i, pais in enumerate(paises, start=1):
            print(f"{i}. {pais}")

        opcao = int(input("Digite o número do país desejado: "))
        pais_escolhido = paises[opcao - 1]

        print(f"\nFilmes do país: {pais_escolhido}\n")
        filmes = listar_filmes_por_pais(pais_escolhido)
        if filmes:
            for titulo in filmes:
                print(f" - {titulo}")
        else:
            print("Nenhum filme encontrado.")


#OPÇÃO PARA LISTAR OS FILMES DE CADA ANO
    if opcoes == "5":

        anos = listar_anos_unicos()
        print("Escolha um ano da lista:")
        for i, ano in enumerate(anos, start=1):
            print(f"{i}. {ano}")

        opcao = int(input("Digite o número do ano desejado: "))
        ano_escolhido = anos[opcao - 1]

        print(f"\nFilmes do ano: {ano_escolhido}\n")
        filmes = listar_filmes_por_ano(ano_escolhido)
        if filmes:
            for titulo in filmes:
                print(f" - {titulo}")
        else:
            print("Nenhum filme encontrado.")

            break
