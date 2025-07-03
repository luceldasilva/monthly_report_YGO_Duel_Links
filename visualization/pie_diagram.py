import pandas as pd
from typing import Sequence, List
from visualization import save_plot
import matplotlib.pyplot as plt
import seaborn as sns


def comparation_pie_diagram(
    count_groupby: List[int],
    labels: Sequence[str],
    pastel_colors: List[str],
    title_pie: str,
    fontsize: int,
    text_center: str
):
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

    ax.set_title(
        title_pie,
        fontsize=28,
        fontweight="bold"
    )
    
    save_plot()
    
    plt.show()



def percentage_deck_popularity(
    decks_sum: pd.DataFrame, limit: int
):
    user_topfive = decks_sum[0:limit].total.sum()
    other_user_decks = decks_sum[limit::].total.sum()
    count_groupby_decks = [int(user_topfive), int(other_user_decks)]
    labels = f"Top {limit} mazos \n más usados", "Resto\n de mazos"
    pastel_colors = ["#ffc59e", "#8CF8D8"]
    title_pie = "Comparativa Top 5\nvs Resto de mazos"
    fontsize, text_center = 24, 'registros'
    
    comparation_pie_diagram(
        count_groupby=count_groupby_decks,
        labels=labels,
        pastel_colors=pastel_colors,
        title_pie=title_pie,
        fontsize=fontsize,
        text_center=text_center
    )