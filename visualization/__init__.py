from queries_db.constants import comunity_dict, comunidades
import queries_db.transform_df_queries as dft
import requests as req
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from wordcloud import WordCloud
import seaborn as sns
import squarify


def comunity_bars(pivot_comunidad: pd.DataFrame):
    
    pivot_comunidad_rename = pivot_comunidad.rename(
        index=comunity_dict
    )


    plt.figure(figsize=(6, 4))

    colors_top_five = [
        '#0000ff', '#808080', '#808080', '#808080', '#808080', '#808080'
    ]

    ax = sns.barplot(
        x=pivot_comunidad_rename.Jugadores, 
        y=pivot_comunidad_rename.index, orient='h',
        joinstyle='bevel'
    )

    new_patches = []
    for patch, color, canal_yt, total in zip(
        ax.patches, colors_top_five, pivot_comunidad.index,
        pivot_comunidad.Jugadores
    ):
        
        bb = patch.get_bbox()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin), abs(bb.width), abs(bb.height),
            boxstyle='round,pad=-0.05,rounding_size=0.73',
            ec='none', fc=color, mutation_aspect=0.73
        )
        patch.remove()
        new_patches.append(p_bbox)

        ax.annotate(
            f'{total}',
            xy=(patch.get_width(), patch.get_y() + patch.get_height()/2),
            xytext=(-5,0), textcoords='offset points',
            arrowprops=dict(arrowstyle='-', color='none'),
            color='white', fontweight='bold', fontsize=12, ha='right', va='center',
            xycoords='data',
            bbox=dict(facecolor='none', edgecolor='none', pad=0),
            annotation_clip=False
        )

    for patch in new_patches:
        ax.add_patch(patch)

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([])
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.title(
        'Registro de usuarios por comunidad',
        fontsize=14, fontweight='bold', x=0.35
    )

    plt.show()



def date_lineplot(
    date_df: pd.DataFrame,
    month_fact_table: str,
    year_fact_table: str,
    tournament_text: str
):
    plt.figure(figsize=(10, 5))

    sns.lineplot(
        data=date_df,
        x='day_of_monthy', y='jugadores',
        marker='o'
    )

    sns.despine(top=True, right=True) 

    plt.xticks(date_df.day_of_monthy)
    plt.xlabel(f"Días de {month_fact_table} {year_fact_table}")
    plt.ylabel("Jugadores")
    plt.title(
        f"Llegadas a {tournament_text} por día",
        fontsize=16,
        fontweight='bold'
    )

    plt.show()


def top_five_decks(
    avatar_bool: bool,
    decks_sum: pd.DataFrame,
    tournament_text: str,
    month_fact_table: str,
    year_fact_table: str,
    kog_df: pd.DataFrame
):
    
    decks_sum = dft.decks_with_avatar(decks_sum)
    
    avatar_deck = decks_sum['url_image']
    del decks_sum['url_image']
    
    plt.figure(figsize=(6, 4))

    colors_top_five = ['#4c2882', '#808080', '#808080', '#808080', '#808080']

    ax = sns.barplot(
        x=decks_sum.total, 
        y=decks_sum.deck, orient='h',
        joinstyle='bevel'
    )

    new_patches = []
    for patch, color, total, avatar in zip(
        ax.patches, colors_top_five, decks_sum['total'], avatar_deck
    ):
        
        bb = patch.get_bbox()
        p_bbox = FancyBboxPatch(
            (bb.xmin, bb.ymin), abs(bb.width), abs(bb.height),
            boxstyle='round,pad=-0.05,rounding_size=0.73',
            ec='none', fc=color, mutation_aspect=0.73
        )
        patch.remove()
        new_patches.append(p_bbox)
        
        if avatar_bool: 
            response = req.get(avatar)
            image = plt.imread(BytesIO(response.content))
            imagebox = OffsetImage(image, zoom=0.8)
            ab = AnnotationBbox(
                imagebox, xy=(2.65, patch.get_y() + patch.get_height()/2),
                xybox=(0,0), xycoords='data', boxcoords="offset points",
                pad=0, arrowprops=dict(arrowstyle='-', color='none'),
                bboxprops=dict(facecolor='none', edgecolor='none')
            )
            ax.add_artist(ab)

        ax.annotate(
            f'{total}',
            xy=(patch.get_width(), patch.get_y() + patch.get_height()/2),
            xytext=(-5,0), textcoords='offset points',
            arrowprops=dict(arrowstyle='-', color='none'),
            color='white', fontweight='bold', fontsize=12, ha='right', va='center',
            xycoords='data',
            bbox=dict(facecolor='none', edgecolor='none', pad=0),
            annotation_clip=False
        )

    for patch in new_patches:
        ax.add_patch(patch)

    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([])
    ax.yaxis.grid(False)
    ax.xaxis.grid(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.title(
        f'Mazos más usados en {tournament_text} {month_fact_table} {year_fact_table}',
        fontsize=14, fontweight='bold', x=0.35
    )

    ax.text(
        0.98, 0.02, f'{len(kog_df)}\nRegistros',
        ha='right', va='bottom', transform=ax.transAxes,
        fontsize=12, fontweight='bold'
    )

    ax.text(
        0.75, 0.02, f'{kog_df.deck.nunique()}\nMazos distintos',
        ha='right', va='bottom', transform=ax.transAxes,
        fontsize=12, fontweight='bold'
    )

    plt.show()


def wordcloud(kog_df: pd.DataFrame, decks_sum: pd.DataFrame):

    top_five_decks = decks_sum.name.iloc[:5].tolist()

    decks = kog_df.drop(kog_df[kog_df['deck'].isin(top_five_decks)].index)


    decks = decks.replace("-", ' ', regex=True)
    decks = decks.replace("/", ' ', regex=True)
    decks = decks.replace(" ", '', regex=True)


    text_decks = ' '.join(decks.fillna('')['deck'].tolist())

    wc = WordCloud(
        width = 2560,
        height = 1440,
        background_color = "mintcream",
        colormap = "Dark2"
    ).generate(text_decks)


    plt.axis("off")
    plt.imshow(wc, interpolation = "bilinear")
    plt.show()


def squarify_decks(
    decks_sum: pd.DataFrame,
    tournament_text: str,
    month_fact_table: str,
    year_fact_table: str
):
    top_ten_decks = decks_sum.iloc[:10]

    otros = decks_sum.iloc[10:].sum()
    otros['name'] = 'Otros'
    top_ten_decks = pd.concat([top_ten_decks, otros.to_frame().T], ignore_index=True)

    labels = [f"{deck}\n{total:.0f}" for deck, total in zip(top_ten_decks["name"], top_ten_decks['total'])]


    fig, ax = plt.subplots(figsize=(6, 4))

    squarify.plot(
        sizes=top_ten_decks.total,
        pad=2,
        label=labels, alpha=.8,
        color=sns.color_palette("Spectral", len(top_ten_decks))
    )

    ax.set_title(f'Mazos reportados a {tournament_text} {month_fact_table} {year_fact_table}')
    ax.axis('off')
    plt.tight_layout()
    plt.show()
