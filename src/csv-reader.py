# import csv

# with open('MSC-1100205EX-2022-07.csv') as arquivo_csv:
#   leitor_csv = csv.DictReader(arquivo_csv)
#   contador_linha = 0
#   for linha in leitor_csv:
#     if contador_linha == 0:
#       print(f'{linha} ')
      
#     if contador_linha == 1:
#       print(f'Os nomes das colunas são {", ".join(linha)}')
#     contador_linha +=1
#     print(f'\t{linha["CONTA"]} ')

import pandas

df = pandas.read_csv('MSC-1100205EX-2022-07.csv', header=1, sep=';')
print(df)