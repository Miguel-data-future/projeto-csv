🎯 Objective
Manage and query Netflix titles (movies and TV shows) from a CSV file, validating the data and storing it in a SQLite database for interactive menu-based queries.

🛠️ Structure
Libraries:

csv → read CSV file

sqlite3 → database management

pydantic → data validation

Database:

Create netflix table

Insert validated records

Replace null values with "Unknown"

Main Functions:

listar_titulos() → all titles

listar_titulos_por_tipo(tipo) → titles by type

listar_titulos_com_info(tipo) → titles with year and country

quant_titulos(tipo) → count movies/TV shows

listar_paises_unicos() → unique countries

listar_filmes_por_pais(pais) → movies by country

listar_anos_unicos() → unique years

listar_filmes_por_ano(ano) → movies by year

Interactive Menu (infinite loop):

List all titles

List by type (movie/TV show)

Count titles

Movies by country

Movies by year

Exit

📊 Flow
CSV → validation with Pydantic → insert into database

Update null fields

User interacts with menu

Queries executed and results shown in console

Loop returns to menu until user exits

✅ Example
Option 4: lists countries → user selects → shows movies from that country

Option 5: lists years → user selects → shows movies from that year