import pandas as pd
from plotly.subplots import make_subplots
from queries_db.constants import data_path, today


def indicator(
    save_photo: bool,
    kc_cup_bool: bool,
    fact_table_df: pd.DataFrame,
    decks_sum: pd.DataFrame,
    fact_table_previous_df: pd.DataFrame,
    comunity: str | None = None
):
    """
    Indicadores para contar el total de mazos distintos
    y comparar con el mes/copa kc anterior la cantidad de registros

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen en outputs
    kc_cup_bool : bool
        Diferenciar entre mes de kog o torneo copa KC
    fact_table_df : pandas.DataFrame
        Mes/copa kc a estudiar
    decks_sum : pandas.DataFrame
        Cantidad de mazos usados en `fact_table_df`
    fact_table_previous_df : pandas.DataFrame
        El mes/copa kc anterior al `fact_table_df`
    comunity : str | None, optional
        Para separar por comunidad al usar con save_photo,
        por defecto es `None` para usar en el general
    """
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
    
    mes: str = 'copa KC' if kc_cup_bool else 'mes'
        
    fig.add_annotation(
        text=f"<span style='font-size:12px; color:{color_relative}'>vs. {mes} anterior</span>",
        x=0.90, y=0.26,
        xref="paper", yref="paper",
        showarrow=False,
        align="center"
    )

    if save_photo:
        comunity_name: str = f'_{comunity}' if comunity else ''
        fig.write_image(f"{data_path}/{today}{comunity_name}_fig_indicator.png")
    
    fig.show()