import pandas as pd
from plotly.subplots import make_subplots
from queries_db.constants import data_path, today


def indicator(
    kog_df: pd.DataFrame,
    decks_sum: pd.DataFrame,
    kog_previous_df: pd.DataFrame
):
    count_kog_previous_df = len(kog_previous_df)

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
        value=len(kog_df),
        title="Registros",
        delta={
            'reference': count_kog_previous_df,
            'relative': True,
            'valueformat': ".1%"
        },
        row=1, col=2
    )

    fig.write_image(f"{data_path}/{today}_fig_indicator.png")
    
    fig.show()