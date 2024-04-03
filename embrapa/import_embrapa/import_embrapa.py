import sqlite3

import pandas as pd

pd.set_option('future.no_silent_downcasting', True) 

table_names = [
    'producao',
    'processamento',
    'comercializacao',
    'importacao',
    'exportacao',
]


def import_csv_site_embrapa():

    urls = [
        'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv',
        'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
        'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv',
        'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
        'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv',
    ]

    for url, table_name in zip(urls, table_names):

        if table_name == 'processamento':
            dados = pd.read_csv(url, sep='\t')
            # Substindo os valores NA e *  nas colunas '2019' e '2022' por 0
            dados['2019'].replace('nd', 0, inplace=True)
            dados['2019'].fillna(0, inplace=True)
            dados['2022'].replace('*', 0, inplace=True)
            dados['2022'].fillna(0, inplace=True)
        else:
            dados = pd.read_csv(url, sep=';')

        conn = sqlite3.connect('db.sqlite3')

        if table_name == 'importacao' or table_name == 'exportacao':
            dados.rename(
                columns={'País': 'pais'}, inplace=True
            )   # removendo acento para criacao de campo
            # Substituindo valores nulos por 0 nas colunas '1970' e '2022'
            dados.fillna(0, inplace=True)


        if not table_exists(conn, table_name):

            dados.to_sql(table_name, conn, index=False)
        else:

            dados.to_sql(table_name, conn, index=False, if_exists='append')

        conn.close()


def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    return cursor.fetchone() is not None


def import_csv_files_embrapa():

    files = [
        'embrapa/csv_files/Producao.csv',
        'embrapa/csv_files/ProcessaViniferas.csv',
        'embrapa/csv_files/Comercio.csv',
        'embrapa/csv_files/ImpVinhos.csv',
        'embrapa/csv_files/ExpVinho.csv',
    ]

    for url, table_name in zip(files, table_names):
        if table_name == 'processamento':
            dados = pd.read_csv(url, sep='\t')
            # Substindo os valores NA e *  nas colunas '2019' e '2022' por 0
            dados['2019'].replace('nd', 0, inplace=True)
            dados['2019'].fillna(0, inplace=True)
            dados['2022'].replace('*', 0, inplace=True)
            dados['2022'].fillna(0, inplace=True)
        else:

            dados = pd.read_csv(url, sep=';')

        conn = sqlite3.connect('db.sqlite3')  
        
        if table_name == 'importacao' or table_name == 'exportacao':
            dados.rename(
                columns={'País': 'pais'}, inplace=True
            )   # removendo acento para criacao de campo
            # Substituindo valores nulos por 0 nas colunas 'ano_1970_1' e 'ano_2022'
            # Substituindo valores nulos por 0 nas colunas '1970' e '2022'
            dados.fillna(0, inplace=True)
     

        dados.to_sql(table_name, conn, index=False, if_exists='append')

        conn.close()
