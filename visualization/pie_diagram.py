import pandas as pd
from typing import Sequence, List
from visualization import save_plot
import matplotlib.pyplot as plt
import seaborn as sns


def comparation_pie_diagram(
    save_photo: bool,
    count_groupby: List[int],
    labels: Sequence[str],
    pastel_colors: List[str],
    title_pie: str | None,
    fontsize: int,
    text_center: str,
):
    """
    Gráfico de pastel para demostrar el total en el medio
    y como se componen

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    count_groupby : List[int]
        Cantidades de las variables
    labels : Sequence[str]
        Las distintas variables del grupo estudiado
    pastel_colors : List[str]
        Paleta de colores para distinguir las variables
    title_pie : str | None
        Título del gráfico
    fontsize : int
        Número del tamaño de fuente para las variables
    text_center : str
        Descripción del total del grupo estudiado
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, texts, autotexts = ax.pie(
        count_groupby, labels=labels, autopct="%1.0f%%",
        colors=pastel_colors,
        wedgeprops={
            'edgecolor': 'white',
            'linewidth': 1,
            'linestyle': 'solid'
        },
        pctdistance=0.75,
        textprops={'fontsize': fontsize}
    )

    centre_circle = plt.Circle((0, 0), 0.4, fc='white')
    ax.add_artist(centre_circle)

    ax.text(
        0, 0,
        f'{sum(count_groupby)}\n{text_center}',
        ha='center', va='center', fontsize=24
    )

    if title_pie:
        ax.set_title(
            title_pie,
            fontsize=28,
            fontweight="bold"
        )
    
    if save_photo:
        save_plot()
    
    plt.show()



def percentage_deck_popularity(
    save_photo: bool, title_bool: bool, decks_sum: pd.DataFrame, limit: int
):
    """
    Comparativa entre los mazos más usados y el resto demostrando una
    gráfica de pastel con la función `comparation_pie_diagram`

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    title_bool : bool
        Elegir si se desea tener título el gráfico
    decks_sum : pandas.DataFrame
        Dataframe de la cantidad de mazos con sus usuarios
    limit : int
        Corte de la cantidad de mazos para separar en dos grupos
    """
    user_topfive = decks_sum[0:limit].total.sum()
    other_user_decks = decks_sum[limit::].total.sum()
    count_groupby_decks = [int(user_topfive), int(other_user_decks)]
    labels = f"Top {limit} mazos \n más usados", "Resto\n de mazos"
    pastel_colors = ["#ffc59e", "#8CF8D8"]
    if title_bool:
        title_pie = f"Comparativa Top {limit}\nvs Resto de mazos"
    else:
        title_pie = None
    fontsize, text_center = 24, 'registros'
    
    comparation_pie_diagram(
        save_photo=save_photo,
        count_groupby=count_groupby_decks,
        labels=labels,
        pastel_colors=pastel_colors,
        title_pie=title_pie,
        fontsize=fontsize,
        text_center=text_center
    )