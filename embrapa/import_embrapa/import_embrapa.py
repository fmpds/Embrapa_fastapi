import re
import sqlite3
from unidecode import unidecode
import numpy as np
import pandas as pd



class read_dataset(object):
    
    def __init__(self, path:str, dataset:str, cols:list):
        self.path = path
        self.dataset = dataset
        self.cols = cols


    def f_read_datasets(self) -> pd.core.frame.DataFrame:
        '''
            Funcao para ler datasets. Essa metodos pode realizar a leitura de qualquer um 
            dos datasets no site da embrapa.
            
            Parametros:
            - Todos os parametros do construtor.
            
            Retorna:
            - dataframe: DataFrame pandas.
                Dataframe com raw data
        
        '''
        
        if self.dataset == 'comercializacao':
            
            # definindo intervalo de tempos colunas
            time_interval = [str(ano) for ano in range(1970, 2023)]

            header = [*self.cols, *time_interval]
            
            dataframe = pd.read_csv(self.path, header=None, names=header, on_bad_lines='skip', sep = ';')
        
        elif self.dataset == 'processamento':
            dataframe = pd.read_csv(self.path, sep = '\t', encoding='latin-1')
        
        else:
            dataframe = pd.read_csv(self.path, sep = ';')
        
        return dataframe

class etl_methods(object):
    
    def __init__(self, cols, values_unpivot):
        self.cols = cols
        self.values_unpivot = values_unpivot
        
    def f_std_column_names(self, dataframe)-> pd.core.frame.DataFrame:
        '''
            Funcao para padrinizar formato das colunas. Todas os nomes das colunas 
            sao transformados para letras maiuscula.
            
            Parametros:
            - Todos os parametros do construtor.
            dataframe: Dataframe pandas.
                Dataframe output do metodo f_read_datasets

            Retorna:
            - dataframe: DataFrame pandas.
                Dataframe com colunas padronizadas
        '''
        
        new_cols_names = {coluna: unidecode(coluna).upper() for coluna in dataframe.columns}
        
        dataframe = dataframe.rename(columns=new_cols_names)
        
        return dataframe


    def f_unpivot_table(self, dataframe) -> pd.core.frame.DataFrame:
        '''
            Funcao para despivotar as tabelas do site da embrapa. Eu um analise
            das tabelas, notamos que elas se encontravam no formato de tabelas pivo,
            que fica dificil tanto para analises quando para leitura dinamiza das 
            tabelas (como as colunas são os anos, eles teriam que ser alterados ma-
            nualmente nos codigos para inclusão de novos anos)
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe com colunas padronizadas
                
            Retorna:
            - dataframe: DataFrame pandas.
                Dataframe despivotado
        
        '''
        dataframe_unpivot = dataframe.melt(id_vars=self.cols, var_name='ANO', value_name= self.values_unpivot)[[*self.cols, 'ANO', self.values_unpivot]]
        #dataframe_unpivot.drop(['ID'], axis=1, inplace = True)
        
        
        
        #dataframe_unpivot['ID'] = dataframe_unpivot['ID'].astype(str) + '_' + dataframe_unpivot['ANO'].astype(str)
        
        return dataframe_unpivot

    def f_remove_accents(self, dataframe, col_name:str) -> pd.core.frame.DataFrame:
        '''
            Função para remover os acentos dos caracteres de uma coluna
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
            - col_name: str
                Nome da coluna para remoçaõ de acentos
            
            Retorna:
            - dataframe: DataFrame pandas.
                Dataframe despivotado com coluna com valores sem acento
        
        '''
        dataframe[col_name] = dataframe[col_name].apply(lambda x: unidecode(str(x)))
        
        return dataframe


    def f_handling_missing_values(self, dataframe, col_name:str) -> pd.core.frame.DataFrame:
        '''
            Função para tratar valores faltantes. Para colunas do tipo numerico (float
            ou inteiro) os missings ou valores que representem os missings são substitui
            dos por 0, caso contrario por '-'
        
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
            - col_name: str
                Nome da coluna para tratar missings
                
            Retorna:
            - dataframe: DataFrame pandas.
                Dataframe despivotado com coluna com missings tratados
        '''
        if dataframe[col_name].isna().sum() > 0:
            if dataframe[col_name].dtypes == 'int64' or dataframe[col_name].dtypes == 'float64':
                dataframe[col_name] = dataframe[col_name].fillna(0, inplace = False)
            
            else:
                dataframe[col_name] = dataframe[col_name].fillna('-', inplace = False)
        
        return dataframe
    
    
    def f_remove_product_acumul_2(self, dataframe, col_name:str) -> list:
        '''
            Algumas tabelas da embrapa tem a seguinte caracteristica: Dentro da coluna produto 
            temos uma linha que representa o grupo dos produtos seguintes, e seu valor é a soma 
            dos membros desse grupo. Essa função trata essa inconsistencia, marcando para ser 
            removidas as linhas que representam classes de produtos
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
            - col_name: str
                Nome da coluna para tratar Tipo dos vinhos
                
            Retorna:
            - rows_to_remove: list.
                Lista de indexes das linhas para serem removidas
        
        '''
        rows_to_remove = []
        
        for i in range(1, dataframe.shape[0]):
            
            # verifica se valor da linha do produto é Maiusculo e se o seguinte é minusculo
            # isso caracterica linhas que representam classes de vinhos
            if dataframe.at[i-1, col_name][-1].isupper() and dataframe.at[i, col_name][-1].islower():
                rows_to_remove.append(i)

        return rows_to_remove
    

    def f_adjust_final_table(self, dataframe:pd.core.frame.DataFrame, cols_to_drop, cols_to_rename) -> pd.core.frame.DataFrame:
        '''
            Função para renomear e remover colunas. Nota-se que algumas colunas das tabelas representam
            uma copia ou algum ruido. Elas são removidas com essa função
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
            - cols_to_drop: list, None
                Lista de nomes das colunas que serão removidas. Se None, nenhuma coluna pe removida
            - cols_to_rename: dict, None
                Dicionario com mapeamento dos nomes das colunas. Se None, nenhuma coluna é renomeada    
        '''
        
        if cols_to_rename != None:
            dataframe.rename(columns=cols_to_rename, inplace = True)
        
        if cols_to_drop != None:
            dataframe.drop(cols_to_drop, inplace = True, axis = 1)
        
        return dataframe

    def f_correct_types_exp_imp(self, dataframe:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        '''
            Função para definir tipos das tabelas de Imp e Exp.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com tipos definidos de acordo com as caracteristicas do dados
            
        '''
        dataframe['PAIS'] = dataframe['PAIS'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['QUANTIDADE'] = dataframe['QUANTIDADE'].fillna(0).astype('int64')
        dataframe['VALOR'] = dataframe['VALOR'].astype('float64')
    
        return dataframe

    def f_correct_types_generic(self, dataframe:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        '''
            Função para definir tipos das tabelas de comer e prod.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com tipos definidos de acordo com as caracteristicas do dados
            
        '''  
        dataframe['PRODUTO'] = dataframe['PRODUTO'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['LITROS'] = dataframe['LITROS'].astype('int64')
        dataframe['TIPO'] = dataframe['TIPO'].astype(str)
        
        return dataframe
    
    def f_correct_types_proc(self, dataframe:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        '''
            Função para definir tipos das tabelas de proce.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com tipos definidos de acordo com as caracteristicas do dados
            
        '''  
       
        dataframe['CULTIVAR'] = dataframe['CULTIVAR'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['QUANTIDADE'] = dataframe['QUANTIDADE'].astype('int64')
        dataframe['TIPO'] = dataframe['TIPO'].astype(str)
        
        return dataframe



    def f_get_dol_values(self, dataframe:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        '''
            Função para recolher os valores dos anos relacionados ao dinheiro.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com colunas dos anos com valores em dolar
        '''        
        dol = [column for column in dataframe.columns if column.endswith('.1')]
        
        df_dol = dataframe.loc[:, [*self.cols,*dol]]
        
        return df_dol

    def f_get_kg_values(self, dataframe:pd.core.frame.DataFrame)-> pd.core.frame.DataFrame:
        '''
            Função para recolher os valores dos anos relacionados a quantidade.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com colunas dos anos com valores em kg
        '''            
        kg = [column for column in dataframe.columns if not column.endswith('.1')]
        
        df_kg = dataframe.loc[:, kg]
        
        return df_kg

    def f_remove_dot_1(self, df_dol:pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        '''
            Função para tratar colunas de quantidade de dolares. Remover .1.
            
            Parametros:
            - Todos os parametros do construtor.
            - dataframe: Dataframe pandas.
                Dataframe depivotado
                
            Retorna:
            - dataframe: Dataframe pandas.
                Dataframe com colunas dos anos com valores em dolares tratadas
        '''          
        columns_adjusted = [column.replace('.1', '') for column in list(df_dol.columns)]
        
        df_dol.columns = columns_adjusted
        
        return df_dol

def f_adjust_table(df, cols, values_unpivot, dataset:dict) -> pd.core.frame.DataFrame:
    
    def f_create_type_product(row, column):
        if row[column][-1].isupper():
            return row[column]
        else:
            return np.nan
    
    
    etl_comer = etl_methods(cols=cols, values_unpivot=values_unpivot)
    
    
    df = etl_comer.f_std_column_names(df)
    
    df_unpivot = etl_comer.f_unpivot_table(dataframe=df)
    
    
    column =str(list(dataset.values())[0])
    
    df_unpivot['TIPO'] =  df_unpivot.apply(lambda row: f_create_type_product(row, column), axis=1)
    df_unpivot['TIPO'] = df_unpivot['TIPO'].ffill()
    
    
    rows_to_remove = etl_comer.f_remove_product_acumul_2(df_unpivot, column)
    
    rows_to_remove = [x - 1 for x in rows_to_remove]
    df_unpivot.drop(rows_to_remove, inplace = True)
    
    df_unpivot['ID'] = range(0, len(df_unpivot['ID']))
    df_unpivot['ID'] = df_unpivot['ID'].astype(str) + df_unpivot['ANO'].astype(str)
    
    def f_replace_by_zero(value):
        '''
            Funcao para remover qualquer conjunto de caracteres de uma coluna
            numerica.
            
            Parametros:
            - value: str
            
            Retorna:
            - subsituit valor por zero se padrão de caracteres for identificado
        
        '''
        
        import re
        
        pattern = re.compile(r'[a-zA-Z*]+')
        
        return re.sub(pattern, '0', value)
    
    
    
    if str(list(dataset.keys())[0]) == "comercializacao":
                
        df_final = etl_comer.f_adjust_final_table(df_unpivot, ['PRODUTO1'], {'PRODUTO2':'PRODUTO'})
    
        df_final = etl_comer.f_correct_types_generic(df_final)
    elif str(list(dataset.keys())[0]) == "processamento":
        df_final = etl_comer.f_adjust_final_table(df_unpivot, ['CONTROL'], None)
        
        df_final['QUANTIDADE'] = df_final['QUANTIDADE'].astype(str).apply(f_replace_by_zero)
        
        df_final = etl_comer.f_correct_types_proc(df_final)
    else:
        df_final = etl_comer.f_adjust_final_table(df_unpivot, None, None)
    
        df_final = etl_comer.f_correct_types_generic(df_final)
    
    
    cols_to_handle_missing =  list(df_final.columns)
        
    for col in cols_to_handle_missing:
        df_final = etl_comer.f_handling_missing_values(df_final, col_name=col)
        
    return df_final


def f_adjust_exp_imp_table(df_exp_imp, cols, values_unpivot):
    
    etl_exp_imp = etl_methods(cols=cols, values_unpivot=values_unpivot)
    
    
    df_exp_imp = etl_exp_imp.f_std_column_names(df_exp_imp)
    
    
    df_exp_kg = etl_exp_imp.f_get_kg_values(df_exp_imp)
    df_exp_dol = etl_exp_imp.f_get_dol_values(df_exp_imp)
    df_exp_dol = etl_exp_imp.f_remove_dot_1(df_exp_dol)

    df_exp_kg_unpivot = etl_exp_imp.f_unpivot_table(dataframe=df_exp_kg)
    df_exp_dol_unpivot = etl_exp_imp.f_unpivot_table(dataframe=df_exp_dol)
    
    df_exp_dol_unpivot.rename(columns = {"QUANTIDADE": "VALOR"}, inplace = True)
    

    df_exp_merge = df_exp_kg_unpivot.merge(df_exp_dol_unpivot, how = 'inner', on = ['ID', 'PAIS', 'ANO'])

    df_exp_merge = etl_exp_imp.f_remove_accents(df_exp_merge, 'PAIS')

    df_exp_merge = etl_exp_imp.f_correct_types_exp_imp(df_exp_merge)
    
    df_exp_merge['ID'] = range(0, len(df_exp_merge['ID']))
    df_exp_merge['ID'] = df_exp_merge['ID'].astype(str) + df_exp_merge['ANO'].astype(str)
    
    cols_to_handle_missing =  list(df_exp_merge.columns)
    for col in cols_to_handle_missing:
        df_exp_merge = etl_exp_imp.f_handling_missing_values(dataframe=df_exp_merge, col_name=col)
        
    return df_exp_merge


pd.set_option('future.no_silent_downcasting', True)


def import_csv_site_embrapa():
    '''
        Descrição bla bla.
        
        Parameters:
        
        Returns:
    '''
 
    paths = {"comercializacao":"http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv",
             "producao":"http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
             "processamento":"http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv",
             "exportacao":"http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv",
             "importacao":"http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv"}
    
    conn = sqlite3.connect('db.sqlite3')
    
    for dataset in list(paths.keys()):
    
        if dataset == "comercializacao":
            cols = ['ID', 'PRODUTO1', 'PRODUTO2']
            datasets_columns = {"comercializacao": "PRODUTO2"}
            values_unpivot = "LITROS"
            
            read = read_dataset(path=paths[dataset], dataset=dataset, cols=cols)

            df_comer = read.f_read_datasets()
            df_final = f_adjust_table(df_comer, cols=cols, values_unpivot=values_unpivot, dataset=datasets_columns)
            
            #df_comer_final.to_csv("./df_comer_processed.csv", encoding="utf-16")
            
        elif dataset == "producao":
            cols = ['ID', 'PRODUTO']
            datasets_columns = {"producao": "PRODUTO"}
            values_unpivot = "LITROS"
            
            
            read = read_dataset(path=paths[dataset], dataset=dataset, cols=cols)

            df_prod = read.f_read_datasets()
            df_final = f_adjust_table(df_prod, cols=cols, values_unpivot=values_unpivot, dataset=datasets_columns)

            #df_prod_final.to_csv("./df_prod_processed.csv", encoding="utf-16")

        elif dataset == "processamento":
            cols = ['ID', 'CONTROL', 'CULTIVAR']
            datasets_columns = {"processamento": "CULTIVAR"}
            values_unpivot = "QUANTIDADE"
            
            
            read = read_dataset(path=paths[dataset], dataset=dataset, cols=cols)

            df_proc = read.f_read_datasets()
            df_final = f_adjust_table(df_proc, cols=cols, values_unpivot=values_unpivot, dataset=datasets_columns)
            
            #df_proc_final.to_csv("./df_proc_processed.csv", encoding="utf-16")
            
        elif dataset == "exportacao":
            cols = ['ID', 'PAIS']
            values_unpivot = "QUANTIDADE"
            
            
            read = read_dataset(path=paths[dataset], cols=cols, dataset=dataset)

            df_exp = read.f_read_datasets()

            df_final = f_adjust_exp_imp_table(df_exp, cols=cols, values_unpivot=values_unpivot)
            
            #df_exp_final.to_csv("./df_exp_processed.csv", encoding="utf-16")
            
        elif dataset == "importacao":
            cols = ['ID', 'PAIS']
            values_unpivot = "QUANTIDADE"
             
            read = read_dataset(path=paths[dataset], cols=cols, dataset=dataset)

            df_imp = read.f_read_datasets()

            df_final = f_adjust_exp_imp_table(df_imp, cols=cols, values_unpivot=values_unpivot)
    
            #df_imp_final.to_csv("./df_imp_processed.csv", encoding="utf-16")       

        if not table_exists(conn, dataset):

            df_final.to_sql(dataset, conn, index=False)
            #conn.close()
        else:

            df_final.to_sql(dataset, conn, index=False, if_exists='replace')
            #conn.close()
        #


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

