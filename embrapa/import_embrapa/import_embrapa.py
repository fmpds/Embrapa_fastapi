import re
import sqlite3
from unidecode import unidecode
import numpy as np
import pandas as pd



def f_read_datasets(dataset:str, path:str, cols:list) -> pd.core.frame.DataFrame:
    
    if dataset == 'comercializacao':
        
        time_interval = [str(ano) for ano in range(1970, 2023)]

        header = [*cols, *time_interval]
        dataframe = pd.read_csv(path, header=None, names=header, on_bad_lines='skip', sep = ';')
    elif dataset == 'processamemto':
        dataframe = pd.read_csv(path, sep = '\t')
    else:
        dataframe = pd.read_csv(path, sep = ';')
        
        
    return dataframe

def f_std_column_names(dataframe:pd.core.frame.DataFrame)-> pd.core.frame.DataFrame:
    
    
    #print(dataframe.columns)
    novos_nomes_colunas = {coluna: unidecode(coluna).upper() for coluna in dataframe.columns}
    
    #print(novos_nomes_colunas)
    dataframe = dataframe.rename(columns=novos_nomes_colunas)
    
    return dataframe



def f_unpivot_table(cols:list, dataframe_adjusted:pd.core.frame.DataFrame, values=str) -> pd.core.frame.DataFrame:
    '''
    
    
    '''
    dataframe_unpivot = dataframe_adjusted.melt(id_vars=cols, var_name='ANO', value_name= values)[[*cols, 'ANO', values]]
    dataframe_unpivot.drop(['ID'], axis=1, inplace = True)
    
    return dataframe_unpivot

def f_remove_accents(df_exp_merge:pd.core.frame.DataFrame,  col_name:str) -> pd.core.frame.DataFrame:
    '''
        Função para remover os acentos dos caracteres
    
    '''
    df_exp_merge[col_name] = df_exp_merge[col_name].apply(lambda x: unidecode(str(x)))
    
    return df_exp_merge

def f_handling_missing_values(dataframe:pd.core.frame.DataFrame, col_name:str) -> pd.core.frame.DataFrame:
    '''
        Função para tratar valores faltantes 
    
    '''

    if dataframe[col_name].isna().sum() > 0:
        if dataframe[col_name].dtypes == 'int64' or dataframe[col_name].dtypes == 'float64':
            dataframe[col_name].fillna(0, inplace = True)
        else:
            dataframe[col_name].fillna('-', inplace = True)
    
    df = dataframe.copy()
    
    return df



def f_get_dol_values(dataframe:pd.core.frame.DataFrame, cols:list) -> pd.core.frame.DataFrame:
    
    dol = [column for column in dataframe.columns if column.endswith('.1')]
    
    df_exp_dol = dataframe.loc[:, [*cols,*dol]]
    
    return df_exp_dol

def f_get_kg_values(dataframe:pd.core.frame.DataFrame)-> pd.core.frame.DataFrame:
    
    kg = [column for column in dataframe.columns if not column.endswith('.1')]
    
    df_exp_kg = dataframe.loc[:, kg]
    
    return df_exp_kg

def f_remove_dot_1(df_exp_dol:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    
    columns_adjusted = [column.replace('.1', '') for column in list(df_exp_dol.columns)]
    
    df_exp_dol.columns = columns_adjusted
    
    return df_exp_dol

def f_create_type_product(row, coluna):
    if row[coluna][-1].isupper():
        return row[coluna]
    else:
        return np.nan
    
def f_remove_product_acumul(dataframe:pd.core.frame.DataFrame, col:str) -> pd.core.frame.DataFrame:
    
    def f_last_uppercase(valor):
        return valor[-1].isupper() if isinstance(valor, str) else False
    
    rows_to_remove = dataframe[col].apply(f_last_uppercase)
    
    dataframe = dataframe[~rows_to_remove]
    
    return dataframe


def f_adjust_comer_table(self) -> pd.core.frame.DataFrame:
    
    df_exp = f_std_column_names()
    
    df_exp_kg = f_get_kg_values()
    df_exp_dol = f_get_dol_values()
    df_exp_dol = f_remove_dot_1(df_exp_dol)
    
    df_exp_kg_adjusted = f_unpivot_table(values='QUANTIDADE (KG)')
    df_exp_dol_adjusted = f_unpivot_table(values='VALOR (USA)')
    
    df_exp_merge = df_exp_kg_adjusted.merge(df_exp_dol_adjusted, how = 'inner', on = ['PAIS', 'ANO'])
    
    df_exp_merge = f_remove_accents(df_exp_merge, 'PAIS')
    
    cols_to_handle_missing =  list(df_exp_merge.columns)
    
    for col in cols_to_handle_missing:
        df_exp_merge = f_handling_missing_values(col_name=col)
    
    return df_exp_merge


def f_adjust_final_table(dataframe:pd.core.frame.DataFrame, cols_to_drop:list, cols_to_rename:dict) -> pd.core.frame.DataFrame:
    dataframe.rename(columns=cols_to_rename, inplace = True)
    
    dataframe.drop(cols_to_drop, inplace = True, axis = 1)
    
    return dataframe
    




pd.set_option('future.no_silent_downcasting', True)

table_names = [
    'producao',
    'processamento',
    'comercializacao',
    'importacao',
    'exportacao',
]


def import_csv_site_embrapa():
    '''
        Descrição bla bla.
        
        Parameters:
        
        Returns:
    '''

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
            dados['Ano'].replace('nd', 0, inplace=True)
            dados['Ano'].fillna(0, inplace=True)
            dados['Ano'].replace('*', 0, inplace=True)
            dados['Ano'].fillna(0, inplace=True)
        elif table_name == 'comercializacao':
            anos = [str(ano) for ano in range(1970, 2023)]
            header = ['Id', 'Produto2', 'Produto'] + anos
            dados = pd.read_csv(url, sep=';', names=header)
            dados = dados.drop('Produto2', axis=1)
        else:
            dados = pd.read_csv(url, sep=';')
        
        conn = sqlite3.connect('db.sqlite3')

        if table_name == 'importacao' or table_name == 'exportacao':
            dados.rename(
                columns={'País': 'pais'}, inplace=True
            )   # removendo acento para criacao de campo
            # Substituindo valores nulos por 0 nas colunas '1970' e '2022'
            dados.fillna(0, inplace=True)
            regex1 = re.compile('^\d{4}\.\d$')
            regex2 = re.compile('\d{4}')

            for header in dados.columns:
                if regex1.match(header):
                    nome_header = 'Valor_' + header[:4]
                    dados.rename(columns={header: nome_header}, inplace=True)
                elif regex2.match(header):
                    nome_header = 'Quantidade_' + header
                    dados.rename(columns={header: nome_header}, inplace=True)

        if not table_exists(conn, table_name):

            dados.to_sql(table_name, conn, index=False)
        else:

            dados.to_sql(table_name, conn, index=False, if_exists='append')

        conn.close()


def table_exists(conn, table_name):
    '''
        Descrição
        
        Parameters
        
        Returns
    '''
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
        elif table_name == 'comercializacao':
            anos = [str(ano) for ano in range(1970, 2023)]
            header = ['Id', 'Produto2', 'Produto'] + anos
            dados = pd.read_csv(url, sep=';', names=header)
            dados = dados.drop('Produto2', axis=1)
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
            regex1 = re.compile('^\d{4}\.\d$')
            regex2 = re.compile('\d{4}')

            for header in dados.columns:
                if regex1.match(header):
                    nome_header = 'Valor_' + header[:4]
                    dados.rename(columns={header: nome_header}, inplace=True)
                elif regex2.match(header):
                    nome_header = 'Quantidade_' + header
                    dados.rename(columns={header: nome_header}, inplace=True)

        dados.to_sql(table_name, conn, index=False, if_exists='append')

        conn.close()
