from queries_db.constants import tables_db
from queries_db import dataframe_queries as dfq
from enum import IntEnum
import locale


class ExcelConstants(IntEnum):
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



locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

fact_table: str = tables_db[-1]
alias_fact_table: str = fact_table[-3:]
kc_cup_bool: bool = False
tournament_text: str = 'DLv. MAX' if kc_cup_bool else 'KOG'

kog_df = dfq.df_query(fact_table, alias_fact_table)

date_fact_table = kog_df.ndmax[0]
month_fact_table: str = date_fact_table.strftime('%B').capitalize()
year_fact_table: str = date_fact_table.strftime('%Y')

df_name: str = f"{tournament_text} {month_fact_table} {year_fact_table}"


if __name__ == "__main__":
    import pygwalker as pyg
    
    
    pyg.walk(kog_df, df_name=df_name)