import csv

with open('netflix_titles.csv', 'r', encoding='utf-8') as file:
        ler_csv = csv.reader(file)
        for row in ler_csv:
            print(row)
