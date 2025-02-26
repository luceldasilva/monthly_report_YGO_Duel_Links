import pandas as pd
import plotly.graph_objects as go
from queries_db.constants import tables_db
from queries_db import dataframe_queries as dfq


def indicator(
    kog_df: pd.DataFrame, month_fact_table: str, year_fact_table: str
):
    kog_previous_df = dfq.df_query(
        tables_db[-2], tables_db[-2][-3:]
    )
    
    count_kog_previous_df = len(kog_previous_df)

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        title = {'text': f'<br>Registros de {month_fact_table} {year_fact_table}</br><span style="font-size:0.8em;color:gray">Comparación al mes anterior</span>'},
        value = len(kog_df),
        delta = {
            'reference': count_kog_previous_df,
            'relative': True,
            'position' : "top",
            'valueformat': ".1%"
        })
    )

    fig.show()