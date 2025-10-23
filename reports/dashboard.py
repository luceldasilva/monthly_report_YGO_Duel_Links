import click
from queries_db import dataframe_queries as dfq
from reports.utils import fact_table_text, build_fact_df
import pygwalker as pyg


@click.command()
@click.option("--kc-cup", is_flag=True, help="Para usar en Copas KC")
def dashboard(kc_cup):
    fact_table, tournament_text, alias_fact_table = build_fact_df(kc_cup)
    
    fact_df = dfq.df_query(fact_table, alias_fact_table)
    
    _, month_fact_table, year_fact_table = fact_table_text(fact_df)
    
    df_name: str = f"{tournament_text} {month_fact_table} {year_fact_table}"
    
    pyg.walk(fact_df, df_name=df_name)


if __name__ == "__main__":
    dashboard()
