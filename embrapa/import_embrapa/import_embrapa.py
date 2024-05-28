import numpy as np
import pandas as pd
from unidecode import unidecode

from embrapa.database import engine


class read_dataset(object):
    """
    Funções da classe:
        - `__init__`
        - f_read_datasets
    """

    def __init__(self, path: str, dataset: str, cols: list):
        self.path = path
        self.dataset = dataset
        self.cols = cols

    def f_read_datasets(self) -> pd.core.frame.DataFrame:
        """Função para ler datasets. Pode realizar a leitura de qualquer um dos datasets no site da embrapa.

        Args:
            self (Construtor): Todos os parâmetros do construtor.

        Returns:
            Dataframe: Dataframe com raw data
        """

        if self.dataset == 'comercializacao':

            # definindo intervalo de tempos colunas
            time_interval = [str(ano) for ano in range(1970, 2023)]

            header = [*self.cols, *time_interval]

            dataframe = pd.read_csv(
                self.path,
                header=None,
                names=header,
                on_bad_lines='skip',
                sep=';',
            )

        elif self.dataset == 'processamento':
            dataframe = pd.read_csv(self.path, sep='\t', encoding='latin-1')

        else:
            dataframe = pd.read_csv(self.path, sep=';')

        return dataframe


class etl_methods(object):
    """
    Funções da classe:
        - `__init__`
        - f_adjust_final_table
        - f_correct_types_exp_imp
        - f_correct_types_generic
        - f_correct_types_proc
        - f_get_dol_values
        - f_get_kg_values
        - f_handling_missing_values
        - f_remove_accents
        - f_remove_dot_1
        - f_remove_product_acumul_2
        - f_std_column_names
        - f_unpivot_table
    """

    def __init__(self, cols, values_unpivot):
        self.cols = cols
        self.values_unpivot = values_unpivot

    def f_std_column_names(self, dataframe) -> pd.core.frame.DataFrame:
        """Função para padronizar o formato das colunas. Todas os nomes das colunas são transformados para letras maiúscula.

        Args:
            self (Construtor): Todos os parâmetros do construtor.
            dataframe (Dataframe): Dataframe output do metodo f_read_datasets.

        Returns:
            Dataframe: Dataframe com colunas padronizadas.
        """

        new_cols_names = {
            coluna: unidecode(coluna).upper() for coluna in dataframe.columns
        }

        dataframe = dataframe.rename(columns=new_cols_names)

        return dataframe

    # Eu um analise
    # das tabelas, notamos que elas se encontravam no formato de tabelas pivo,
    # que fica dificil tanto para analises quando para leitura dinamiza das
    # tabelas (como as colunas são os anos, eles teriam que ser alterados ma-
    # nualmente nos codigos para inclusão de novos anos)

    def f_unpivot_table(self, dataframe) -> pd.core.frame.DataFrame:
        """Função para despivotar as tabelas do site da embrapa.

        Args:
            self (Construtor): Todos os parâmetros do construtor.
            dataframe (dataframe): Dataframe com colunas padronizadas.

        Returns:
            dataframe_unpivot: Dataframe despivotado.
        """
        dataframe_unpivot = dataframe.melt(
            id_vars=self.cols, var_name='ANO', value_name=self.values_unpivot
        )[[*self.cols, 'ANO', self.values_unpivot]]

        return dataframe_unpivot

    def f_remove_accents(
        self, dataframe, col_name: str
    ) -> pd.core.frame.DataFrame:
        """Função para remover os acentos dos caracteres de uma coluna.

        Args:
            self (Construtor): Todos os parâmetros do construtor.
            dataframe (Dataframe): Dataframe pandas.
            col_name: Nome da coluna para remoção de acentos.

        Returns:
            dataframe: Dataframe com colunas e valores sem acento.
        """
        dataframe[col_name] = dataframe[col_name].apply(
            lambda x: unidecode(str(x))
        )

        return dataframe

    def f_handling_missing_values(
        self, dataframe, col_name: str
    ) -> pd.core.frame.DataFrame:
        """Função para tratar valores faltantes. Para colunas do tipo numerico (float
        ou inteiro) os missings ou valores que representem os missings são substitui
        dos por 0, caso contrario por '-'

        Args:
            self (Construtor): Todos os parâmetros do construtor.
            dataframe (Dataframe): Dataframe pandas.
            col_name: Nome da coluna para tratar missings.

        Returns:
            dataframe: Dataframe com coluna com missings tratados
        """
        if dataframe[col_name].isna().sum() > 0:
            if (
                dataframe[col_name].dtypes == 'int64'
                or dataframe[col_name].dtypes == 'float64'
            ):
                dataframe[col_name] = dataframe[col_name].fillna(
                    0, inplace=False
                )
            else:
                dataframe[col_name] = dataframe[col_name].fillna(
                    '-', inplace=False
                )

        return dataframe

    #    Algumas tabelas da embrapa tem a seguinte caracteristica: Dentro da coluna produto
    #    temos uma linha que representa o grupo dos produtos seguintes, e seu valor é a soma
    #    dos membros desse grupo. Essa função trata essa inconsistencia, marcando para ser
    #    removidas as linhas que representam classes de produtos

    def f_remove_product_acumul_2(self, dataframe, col_name: str) -> list:
        """Função para retirar a linha de soma total de determinados grupos de produtos.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe (Dataframe): Dataframe pandas.
            col_name: Nome da coluna para tratar o tipo dos vinhos

        Returns:
            rows_to_remove: Uma lista de indexes das linhas para serem removidas
        """
        rows_to_remove = []

        for i in range(1, dataframe.shape[0]):

            # verifica se valor da linha do produto é Maiusculo e se o seguinte é minusculo
            # isso caracterica linhas que representam classes de vinhos
            if (
                dataframe.at[i - 1, col_name][-2].isupper()
                and dataframe.at[i, col_name][-2].islower()
            ):
                rows_to_remove.append(i)

        return rows_to_remove

    # Nota-se que algumas colunas das tabelas representam
    # uma copia ou algum ruido. Elas são removidas com essa função

    def f_adjust_final_table(
        self, dataframe: pd.core.frame.DataFrame, cols_to_drop, cols_to_rename
    ) -> pd.core.frame.DataFrame:
        """
        Função para renomear e remover colunas.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe (Dataframe): Dataframe pandas.
            cols_to_drop (list, None): Lista de nomes das colunas que serão removidas. Se None, nenhuma coluna pe removida
            cols_to_rename (dict, None): Dicionario com mapeamento dos nomes das colunas. Se None, nenhuma coluna é renomeada

        Returns:
            dataframe: Dataframe com as colunas renomeadas/removidas determinadas
        """

        if cols_to_rename != None:
            dataframe.rename(columns=cols_to_rename, inplace=True)

        if cols_to_drop != None:
            dataframe.drop(cols_to_drop, inplace=True, axis=1)

        return dataframe

    def f_correct_types_exp_imp(
        self, dataframe: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """Função para definir tipos das tabelas de Imp e Exp.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe (Dataframe): Dataframe pandas.

        Returns:
            dataframe: Dataframe com tipos definidos de acordo com as caracteristicas do dados
        """
        dataframe['PAIS'] = dataframe['PAIS'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['QUANTIDADE'] = (
            dataframe['QUANTIDADE'].fillna(0).astype('int64')
        )
        dataframe['VALOR'] = dataframe['VALOR'].astype('float64')

        return dataframe

    def f_correct_types_generic(
        self, dataframe: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """Função para definir tipos das tabelas de comer e prod.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe (Dataframe): Dataframe pandas.

        Returns:
            dataframe: Dataframe com tipos definidos de acordo com as caracteristicas do dados
        """
        dataframe['PRODUTO'] = dataframe['PRODUTO'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['LITROS'] = dataframe['LITROS'].astype('int64')
        dataframe['TIPO'] = dataframe['TIPO'].astype(str)

        return dataframe

    def f_correct_types_proc(
        self, dataframe: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """Função para definir tipos das tabelas de comercialização e processamento.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe (Dataframe): Dataframe pandas.

        Returns:
            dataframe: Dataframe com tipos definidos de acordo com as caracteristicas do dados
        """

        dataframe['CULTIVAR'] = dataframe['CULTIVAR'].astype(str)
        dataframe['ANO'] = dataframe['ANO'].astype('int64')
        dataframe['QUANTIDADE'] = dataframe['QUANTIDADE'].astype('int64')
        dataframe['TIPO'] = dataframe['TIPO'].astype(str)

        return dataframe

    def f_get_dol_values(
        self, dataframe: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """Função para recolher os valores dos anos relacionados ao dinheiro.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe: Dataframe pandas...

        Returns:
            df_dol: Dataframe...
        """
        dol = [column for column in dataframe.columns if column.endswith('.1')]

        df_dol = dataframe.loc[:, [*self.cols, *dol]]

        return df_dol

    def f_get_kg_values(
        self, dataframe: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:
        """Função para recolher os valores dos anos relacionados a quantidade.

        Args:
            self (Construtor): Todos os parametros do construtor.
            dataframe: Dataframe pandas...

        Returns:
            df_kg: Dataframe...
        """
        kg = [
            column for column in dataframe.columns if not column.endswith('.1')
        ]

        df_kg = dataframe.loc[:, kg]

        return df_kg

    def f_remove_dot_1(
        self, df_dol: pd.core.frame.DataFrame
    ) -> pd.core.frame.DataFrame:

        """Função para retirar colunas que terminam com o sufixo ".1"

        Args:
            self (Construtor): Todos os parametros do construtor.
            df_dol (Dataframe): Dataframe pandas apos passar pelo processamento da função "f_get_dol_values"

        Returns:
            df_dol: Dataframe com as colunas filtradas
        """
        columns_adjusted = [
            column.replace('.1', '') for column in list(df_dol.columns)
        ]

        df_dol.columns = columns_adjusted

        return df_dol


def f_adjust_table(
    df, cols, values_unpivot, dataset: dict
) -> pd.core.frame.DataFrame:
    """Função para ajustar um dataframe com todas as funções dentro de "etl_methods"

    Args:
        df (Dataframe): Dataframe
        cols (object): Colunas do dataframe
        value_unpivot (object): Colunas despivotadas (?)
        dataset: Dataset

    Returns:
        df_final: Dataframe filtrado
    """

    def f_create_type_product(row, column):
        if row[column][-2].isupper():
            return row[column]
        else:
            return np.nan

    etl_comer = etl_methods(cols=cols, values_unpivot=values_unpivot)

    df = etl_comer.f_std_column_names(df)

    df_unpivot = etl_comer.f_unpivot_table(dataframe=df)

    column = str(list(dataset.values())[0])

    df_unpivot['TIPO'] = df_unpivot.apply(
        lambda row: f_create_type_product(row, column), axis=1
    )
    df_unpivot['TIPO'] = df_unpivot['TIPO'].ffill()

    rows_to_remove = etl_comer.f_remove_product_acumul_2(df_unpivot, column)

    rows_to_remove = [x - 1 for x in rows_to_remove]

    df_unpivot.drop(rows_to_remove, inplace=True)

    df_unpivot['ID'] = range(0, len(df_unpivot['ID']))
    df_unpivot['ID'] = df_unpivot['ID'].astype(str) + df_unpivot['ANO'].astype(
        str
    )

    def f_replace_by_zero(value):
        """Função para remover qualquer conjunto de caracteres de uma coluna numerica.

        Args:
            value (str): Uma cadeia de caracteres

        Returns:
            string: Uma cadeia de caracteres sem letras
        """

        import re

        pattern = re.compile(r'[a-zA-Z*]+')

        return re.sub(pattern, '0', value)

    if str(list(dataset.keys())[0]) == 'comercializacao':

        df_final = etl_comer.f_adjust_final_table(
            df_unpivot, ['PRODUTO1'], {'PRODUTO2': 'PRODUTO'}
        )

        df_final = etl_comer.f_correct_types_generic(df_final)
    elif str(list(dataset.keys())[0]) == 'processamento':
        df_final = etl_comer.f_adjust_final_table(
            df_unpivot, ['CONTROL'], None
        )

        df_final['QUANTIDADE'] = (
            df_final['QUANTIDADE'].astype(str).apply(f_replace_by_zero)
        )

        df_final = etl_comer.f_correct_types_proc(df_final)
    else:
        df_final = etl_comer.f_adjust_final_table(df_unpivot, None, None)

        df_final = etl_comer.f_correct_types_generic(df_final)

    cols_to_handle_missing = list(df_final.columns)

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

    df_exp_dol_unpivot.rename(columns={'QUANTIDADE': 'VALOR'}, inplace=True)

    df_exp_merge = df_exp_kg_unpivot.merge(
        df_exp_dol_unpivot, how='inner', on=['ID', 'PAIS', 'ANO']
    )

    df_exp_merge = etl_exp_imp.f_remove_accents(df_exp_merge, 'PAIS')

    # print(df_exp_merge.columns)
    df_exp_merge = etl_exp_imp.f_correct_types_exp_imp(df_exp_merge)

    df_exp_merge['ID'] = range(0, len(df_exp_merge['ID']))
    df_exp_merge['ID'] = df_exp_merge['ID'].astype(str) + df_exp_merge[
        'ANO'
    ].astype(str)

    cols_to_handle_missing = list(df_exp_merge.columns)

    for col in cols_to_handle_missing:
        df_exp_merge = etl_exp_imp.f_handling_missing_values(
            dataframe=df_exp_merge, col_name=col
        )

    return df_exp_merge


pd.set_option('future.no_silent_downcasting', True)


def import_csv_site_embrapa(online: bool):
    """Função para importar os arquivos .csv do site da embrapa

    Parameters:
        online (bool): Em caso True os arquivos .csv serão baixados direto do site da embrapa, em caso de False os arquivos .csv serão carregados a partir de um diretorio local

    """

    if online:
        paths = {
            'comercializacao': 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv',
            'producao': 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv',
            'processamento': 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
            'exportacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv',
            'importacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
        }
    else:
        paths = {
            'comercializacao': 'embrapa/csv_files/Comercio.csv',
            'producao': 'embrapa/csv_files/Producao.csv',
            'processamento': 'embrapa/csv_files/ProcessaViniferas.csv',
            'exportacao': 'embrapa/csv_files/ExpVinho.csv',
            'importacao': 'embrapa/csv_files/ImpVinhos.csv',
        }

    for dataset in list(paths.keys()):

        if dataset == 'comercializacao':
            cols = ['ID', 'PRODUTO1', 'PRODUTO2']
            datasets_columns = {'comercializacao': 'PRODUTO2'}
            values_unpivot = 'LITROS'

            read = read_dataset(
                path=paths[dataset], dataset=dataset, cols=cols
            )

            df_comer = read.f_read_datasets()
            df_final = f_adjust_table(
                df_comer,
                cols=cols,
                values_unpivot=values_unpivot,
                dataset=datasets_columns,
            )

            # df_comer_final.to_csv("./df_comer_processed.csv", encoding="utf-16")

        elif dataset == 'producao':
            cols = ['ID', 'PRODUTO']
            datasets_columns = {'producao': 'PRODUTO'}
            values_unpivot = 'LITROS'

            read = read_dataset(
                path=paths[dataset], dataset=dataset, cols=cols
            )

            df_prod = read.f_read_datasets()
            df_final = f_adjust_table(
                df_prod,
                cols=cols,
                values_unpivot=values_unpivot,
                dataset=datasets_columns,
            )

            # df_prod_final.to_csv("./df_prod_processed.csv", encoding="utf-16")

        elif dataset == 'processamento':
            cols = ['ID', 'CONTROL', 'CULTIVAR']
            datasets_columns = {'processamento': 'CULTIVAR'}
            values_unpivot = 'QUANTIDADE'

            read = read_dataset(
                path=paths[dataset], dataset=dataset, cols=cols
            )

            df_proc = read.f_read_datasets()
            df_final = f_adjust_table(
                df_proc,
                cols=cols,
                values_unpivot=values_unpivot,
                dataset=datasets_columns,
            )

            # df_proc_final.to_csv("./df_proc_processed.csv", encoding="utf-16")

        elif dataset == 'exportacao':
            cols = ['ID', 'PAIS']
            values_unpivot = 'QUANTIDADE'

            read = read_dataset(
                path=paths[dataset], cols=cols, dataset=dataset
            )

            df_exp = read.f_read_datasets()

            df_final = f_adjust_exp_imp_table(
                df_exp, cols=cols, values_unpivot=values_unpivot
            )

            # df_exp_final.to_csv("./df_exp_processed.csv", encoding="utf-16")

        elif dataset == 'importacao':
            cols = ['ID', 'PAIS']

            values_unpivot = 'QUANTIDADE'

            read = read_dataset(
                path=paths[dataset], cols=cols, dataset=dataset
            )

            df_imp = read.f_read_datasets()

            df_final = f_adjust_exp_imp_table(
                df_imp, cols=cols, values_unpivot=values_unpivot
            )

            # df_imp_final.to_csv("./df_imp_processed.csv", encoding="utf-16")

        try:
            df_final.columns = map(str.lower, df_final.columns)
            df_final.to_sql(dataset, engine, index=False, if_exists='append')
        except Exception as e:
            print(e)


def table_exists(conn, table_name):
    """Função para verificar a existencia de tabelas no banco de dados.
    Caso ja haja tabelas existentes com o mesmo nome as tabelas não serão importadas.

    Returns:
        Valor (boolean): True para caso exista e False para caso não exista
    """
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'"
    )
    return cursor.fetchone() is not None
