import pandas as pd
from plotly.subplots import make_subplots
from queries_db.constants import data_path, today


def indicator(
    save_photo: bool,
    fact_table_df: pd.DataFrame,
    decks_sum: pd.DataFrame,
    fact_table_previous_df: pd.DataFrame,
    comunity: str | None = None
):
    fact_count = len(fact_table_df)
    
    count_fact_previous_df = len(fact_table_previous_df)

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{'type': 'indicator'}, {'type': 'indicator'}]]
    )
    
    
    fig.add_indicator(
        mode="number",
        value=len(decks_sum),
        title="Mazos<br>distintos",
        row=1, col=1
    )
    
    fig.add_indicator(
        mode="number+delta",
        value=fact_count,
        title="Registros",
        delta={
            'reference': count_fact_previous_df,
            'relative': True,
            'valueformat': ".1%"
        },
        row=1, col=2
    )
    
    color_relative: str = 'red' if fact_count < count_fact_previous_df else 'green'
    
    fig.add_annotation(
        text=f"<span style='font-size:12px; color:{color_relative}'>vs. mes anterior</span>",
        x=0.9, y=0.24,
        xref="paper", yref="paper",
        showarrow=False,
        align="center"
    )

    if save_photo:
        comunity_name: str = f'_{comunity}' if comunity else ''
        fig.write_image(f"{data_path}/{today}{comunity_name}_fig_indicator.png")
    
    fig.show()