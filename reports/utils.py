from queries_db.constants import tables_db, kc_tables_db
from decouple import Config, RepositoryEnv
from typing import Final
from pathlib import Path
from datetime import date
from enum import IntEnum
import pandas as pd
import locale


class ExcelConstants(IntEnum):
    """
    Para usar en excel representando a sus códigos de VBA
    """
    xlUp = -4162
    xlToLeft = -4159
    xlDatabase = 1
    xlRowField = 1
    xlDataField = 4
    xlSum = -4157
    xlDescending = 2
    xlPercentOfTotal = 8
    xlColumnClustered = 51
    xlLocationAsObject = 2
    xlCount = -4112
    xlBarClustered = 57


def default_avatar() -> str:
    """
    Enlace para usar en arquetipos que aun no tienen avatar

    Returns
    -------
    str
        la url de un avatar en blanco o uno predeterminado
    """
    BASE_DIR = Path(__file__).resolve().parent
    config = Config(RepositoryEnv(str(BASE_DIR / '.env')))
    DEFAULT_URL: Final = config('URL')
    return DEFAULT_URL

DEFAULT_URL = default_avatar()


def build_fact_df(kc_cup: bool, idx_fact_table: int = 1):
    """
    Texto para usar en la función de `df_query`, y usar con click
    
    Parameters
    ----------
    kc_cup: bool
        Para usar la lista de meses de kog o
        la de los meses que se jugaron la copa KC
    
    idx_fact_table: int
        Para indicar el índice de la lista de tablas a usar
        Es el 1 como defecto para usar la última tabla
    
    Returns
    -------
    fact_table: str
        Nombre de la tabla a usar
    tournament_text: str
        Catagolado si es de la Copa KC o KOG
    alias_fact_table: str
        Abreviatura de `fact_table` para usar en las consultas sql
    """
    fact_table: str = kc_tables_db[-idx_fact_table] if kc_cup else tables_db[-idx_fact_table]
    tournament_text: str = 'DLv. MAX' if kc_cup else 'KOG'
    alias_fact_table: str = fact_table[-3:]

    return fact_table, tournament_text, alias_fact_table


def fact_table_text(fact_df: pd.DataFrame, spanish: bool = False):
    """
    Textos para usar sobre el dataframe creado por `df_query`
    
    Parameters
    ----------
    fact_df: DataFrame
        Tabla de hechos a usar
    
    spanish: bool
        Para nombrar los meses en español
    
    Returns
    -------
    date_fact_table: date
        La primera fecha del mes para el dataframe
    month_fact_table: str
        Mes correspondiente al `fact_df`
    year_fact_table: str
        Año correspondiente al `fact_df`
    """
    date_fact_table: date = fact_df.ndmax[0]
    
    if spanish:
        locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')
        #'es_ES.utf8'  En Linux/Mac
    
    month_fact_table: str = date_fact_table.strftime('%B').capitalize()
    year_fact_table: str = date_fact_table.strftime('%Y')
    
    return date_fact_table, month_fact_table, year_fact_table