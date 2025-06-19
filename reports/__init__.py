import pygwalker as pyg
from queries_db.constants import tables_db
from queries_db import dataframe_queries as dfq
import locale


locale.setlocale(locale.LC_TIME, 'Spanish_Spain.1252')

fact_table: str = tables_db[-1]
alias_fact_table: str = fact_table[-3:]
kc_cup_bool: bool = False
tournament_text: str = 'DLv. MAX' if kc_cup_bool else 'KOG'

kog_df = dfq.df_query(fact_table, alias_fact_table)

date_fact_table = kog_df.ndmax[0]

month_fact_table = date_fact_table.strftime('%B').capitalize()
year_fact_table = date_fact_table.strftime('%Y')

df_name: str = f"{tournament_text} {month_fact_table} {year_fact_table}"


pyg.walk(kog_df, df_name=df_name)