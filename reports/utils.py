from queries_db.constants import tables_db, kc_tables_db
from enum import IntEnum
import pandas as pd


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



def build_fact_df(kc_cup: bool):
    """
    Texto para usar en la función de df_query, y suar con click
    """
    fact_table = kc_tables_db[-1] if kc_cup else tables_db[-1]
    tournament_text = 'DLv. MAX' if kc_cup else 'KOG'
    alias_fact_table = fact_table[-3:]

    return fact_table, tournament_text, alias_fact_table


def fact_table_text(fact_df: pd.DataFrame):
    """
    Textos para usar sobre el dataframe creado por df_query
    """
    date_fact_table = fact_df.ndmax[0]
    month_fact_table: str = date_fact_table.strftime('%B').capitalize()
    year_fact_table: str = date_fact_table.strftime('%Y')
    
    return month_fact_table, year_fact_table