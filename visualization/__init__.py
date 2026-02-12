from datetime import datetime
from queries_db.constants import comunity_dict, data_path
import queries_db.transform_df_queries as dft
from reports.utils import fact_table_text, DEFAULT_URL
from queries_db import dataframe_queries as dfq
import requests as req
from io import BytesIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from wordcloud import WordCloud
import seaborn as sns
import squarify
import plotly.express as px
import plotly.graph_objects as go
import circlify


def save_plot():
    """
        Para guardar en fotos los gráficos
    """
    
    today_now = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S_%f')[:-3]}.png"
    
    name_plt = data_path / today_now
    
    plt.savefig(name_plt, bbox_inches='tight')


def comunity_bars(save_photo: bool, pivot_comunidad: pd.DataFrame):
    """
    Gráfico de barras sobre las distintas comunidades y sus registros

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    pivot_comunidad : pandas.DataFrame
        Tabla de las comunidades con su cantidad de registros
    """
    
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

    if save_photo:
        save_plot()
    
    plt.show()



def date_lineplot(
    save_photo: bool,
    date_df: pd.DataFrame,
    month_fact_table: str,
    year_fact_table: str,
    tournament_text: str
):
    """
    Gráfico de líneas mostrando la canitdad de registros por día

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    date_df : pandas.DataFrame
        Tabla de los días del mes estudiado ya sea KOG o copa KC
    month_fact_table : str
        Mes de la tabla estudiada
    year_fact_table : str
        Año de la tabla estudiada
    tournament_text : str
        Catalogado si es del mes KOG o copa KC
    """
    fig = px.line(
        date_df,
        y="day_of_monthy", x="jugadores",
        title= f"LLegadas a {tournament_text} por día",
        text="jugadores",
        template='simple_white',
        labels={
            "day_of_monthy": f"Días de {month_fact_table} {year_fact_table}",
            "jugadores": "Registros"
        }
    )

    fig.update_layout(width=500, height=900)
    fig.update_yaxes(autorange="reversed")
    fig.update_traces(textposition="top center")
    
    if save_photo:
        fig.write_image(
            f"{data_path}/{datetime.now().strftime('%d_%m_%Y_%H_%M_%S_%f')[:-3]}_llegadas_a_{tournament_text}_{month_fact_table}_{year_fact_table}.png"
        )
    
    fig.show()


def top_five_decks(
    save_photo: bool,
    avatar_bool: bool,
    decks_sum: pd.DataFrame,
    limit: int,
    tournament_text: str | None = None,
    month_fact_table: str | None = None,
    year_fact_table: str | None = None
):
    """
    Gráfico de barras de los mazos más populares del mes/copa KC estudiado

    Parameters
    ----------
    save_photo : bool
        Guardar la foto
    avatar_bool : bool
        Usar los avatares de los mazos
    decks_sum : pandas.DataFrame
        Lista total de los mazos más usados con sus registros
        para luego separarlos con `limit` y la función `decks_with_avatar`
    limit : int
        Corte del grupo para separar a los más utilizados
    tournament_text : str | None, optional
        Para usar con el título, texto para contar si es del mes KOG
        o de la copa KC, por defecto es None
    month_fact_table : str | None, optional
        Para usar con el título, mes de la tabla de hechos estudiada,
        por defecto es None
    year_fact_table : str | None, optional
        Para usar con el título, año de la tabla de hechos estudiada,
        por defecto es None
    """
    decks_sum = dft.decks_with_avatar(decks_sum, limit)
    
    avatar_deck = decks_sum['url_image']
    del decks_sum['url_image']
    
    plt.figure(figsize=(6, 4))

    #* Por si hay empate en el puesto 5 se ponen los igualados
    colors_top_five = ['#4c2882'] + ['#808080'] * (len(avatar_deck) - 1)

    ax = sns.barplot(
        x=decks_sum.total, 
        y=decks_sum.deck, orient='h',
        joinstyle='bevel'
    )

    new_patches = []
    x_avatar = None
    num_zoom: float = 0.7 if limit >5 else 0.8
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
            imagebox = OffsetImage(image, zoom=num_zoom)
            if x_avatar is None:
                x_avatar = patch.get_x() + (patch.get_width() * 0.05)
            ab = AnnotationBbox(
                imagebox, xy=(x_avatar, patch.get_y() + patch.get_height()/2),
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

    if tournament_text and month_fact_table and year_fact_table:
        plt.title(
            f'Mazos más usados en {tournament_text} {month_fact_table} {year_fact_table}',
            fontsize=14, fontweight='bold', x=0.35
        )

    if save_photo:
        save_plot()
    
    plt.show()


def wordcloud(
    save_photo: bool,
    fact_table_df: pd.DataFrame,
    decks_sum: pd.DataFrame,
    limit: int
):
    """
    Lista del resto de mazos usados

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    fact_table_df : pandas.DataFrame
        Tabla de hechos a estudiar
    decks_sum : pandas.DataFrame
        Mazos usados en `fact_table_df` con sus registros
    limit : int
        Corte del grupo para separar de los más populares
    """

    top_five_decks = decks_sum.name.iloc[:limit].tolist()

    decks = fact_table_df.drop(
        fact_table_df[fact_table_df['deck'].isin(top_five_decks)].index
    )


    decks = decks.replace("-", ' ', regex=True)
    decks = decks.replace("/", ' ', regex=True)
    decks = decks.replace("’", ' ', regex=True)
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
    
    if save_photo:
        save_plot()
    
    plt.show()


def squarify_decks(
    save_photo: bool,
    decks_sum: pd.DataFrame,
    tournament_text: str,
    month_fact_table: str,
    year_fact_table: str
):
    """
    Gráfico tipo Treemaps del mes/copa KC estudiada
    mostrando los mazos utilizados

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    decks_sum : pandas.DataFrame
        Lista de mazos con sus registros
    tournament_text : str
        Catalogado si es del mes KOG o de la copa KC
    month_fact_table : str
        Mes de la tabla de hechos estudiada
    year_fact_table : str
        Año de la tabla de hechos estudiada
    """
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
    
    if save_photo:
        save_plot()
    
    plt.show()


def circle_packing_chart(
    decks_sum: pd.DataFrame,
    fact_df: pd.DataFrame,
    fact_previous_df: pd.DataFrame,
    month_fact_table: str,
    year_fact_table: str,
    kc_cup_bool: bool = False,
):
    """
    Gráfico tipo Circle Packing del mes/copa KC estudiada
    mostrando los mazos utilizados

    Parameters
    ----------
    decks_sum : pd.DataFrame
        Mazos usados en `fact_table_df` con sus registros
    fact_df: pd.DataFrame
        Registro mensual del mes/copa KC
    fact_previous_df: pd.DataFrame
        Registro mensual del anterior mes/copa KC
    tournament_text : str
        Para usar con el título, texto para contar si es del mes KOG
        o de la copa KC
    month_fact_table : str
        Para usar con el título, mes de la tabla de hechos estudiada
    year_fact_table : str 
        Para usar con el título, año de la tabla de hechos estudiada
    kc_cup_bool : bool, optional
        Para usar en en los títulos si es mes KOG o copa KC,
        por defecto es False
    """

    spanish_tour: str = "DLv. MAX Copa KC" if kc_cup_bool else "King of Games"
    
    title_report: str = f'{spanish_tour} {month_fact_table} {year_fact_table}'
    
    df_count, count_fact_previous = len(fact_df), len(fact_previous_df)

    decks_images = pd.read_json(
        'https://monthly-report-yugioh-dl.vercel.app/decks/',
        orient='records'
    )[['name', 'url_image', 'big_avatar']]

    group_by_decks = decks_sum.merge(
        decks_images, on='name', how='left', validate='1:1'
    )

    group_by_decks['avatar'] = np.where(
        group_by_decks['total'] < 4,
        group_by_decks['url_image'],
        group_by_decks['big_avatar']
    )

    group_by_decks['avatar'] = group_by_decks['avatar'].fillna(DEFAULT_URL)

    color: str = 'red' if df_count < count_fact_previous else 'green'
    tour_text: str = 'Copa KC' if kc_cup_bool else 'mes'
    percentage_count = (
        (df_count - count_fact_previous) / count_fact_previous
    ) * 100
    icon_relative: str = '▼' if df_count < count_fact_previous else '▲'

    circles = circlify.circlify(
        decks_sum['total'].tolist(),
        show_enclosure=False,
        target_enclosure=circlify.Circle(x=0, y=0, r=1)
    )

    circles = circles[::-1]

    fig = go.Figure()

    for circle, name, total, big_avatar  in zip(
        circles, group_by_decks['name'],
        group_by_decks['total'], group_by_decks['avatar']
    ):
        fig.add_trace(go.Scatter(
            x=[circle.x],
            y=[circle.y],
            mode='markers+text',
            marker=dict(
                size=circle.r*500,
                color='rgba(100, 150, 200, 0.3)'
            ),
            textposition='middle center',
            hovertemplate=f'<b>{name}</b><br>Registros: {total}<extra></extra>'
        ))
        
        fig.add_layout_image(
            dict(
                source=big_avatar,
                xref="x",
                yref="y",
                x=circle.x,
                y=circle.y,
                sizex=circle.r * 2,
                sizey=circle.r * 2,
                xanchor="center",
                yanchor="middle",
                opacity=0.8,
                layer="above"
            )
        )

    count_deck: str = f"<b style='font-size:32px'>{len(decks_sum)}</b><br>"
    description_deck: str = "<span style='font-size:14px'>Mazos<br>distintos</span>"
    annotation_decks: str = count_deck + description_deck

    fig.add_annotation(
        text=annotation_decks,
        x=0.1, y=0.95,
        xref="paper", yref="paper",
        showarrow=False,
        align="center",
        xanchor="center",
        yanchor="top",
        bgcolor="rgba(255, 255, 255, 0.8)",
        borderwidth=1,
        borderpad=10
    )

    string_df_count: str = f"<b style='font-size:32px'>{df_count}</b><br>"
    description: str = "<span style='font-size:14px'>Registros</span><br>"
    icon: str = f"<span style='font-size:12px; "
    color_description: str = f"color:{color}'>{icon_relative} "
    percentage: str = f"{abs(percentage_count):.1f}%"
    relative: str = f"<br>vs. {tour_text} anterior</span>"

    annotation_df: str = f"{string_df_count}{description}{icon}"
    annotation_percentage: str = f"{color_description}{percentage}{relative}"

    annotation_counts: str = annotation_df + annotation_percentage

    fig.add_annotation(
        text=annotation_counts,
        x=0.85, y=0.95,
        xref="paper", yref="paper",
        showarrow=False,
        align="center",
        xanchor="center",
        yanchor="top",
        bgcolor="rgba(255, 255, 255, 0.8)",
        borderwidth=1,
        borderpad=10
    )


    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, scaleanchor="y", scaleratio=1),
        yaxis=dict(visible=False),
        width=800,
        height=800,
        plot_bgcolor='white',
        paper_bgcolor='white',
        title=dict(
            text="Distribución de Mazos",
            x=0.5,
            xanchor="center",
            y=0.95,
            yanchor="top",
            font=dict(
                size=24,
                color="black",
                weight=600
            ),
            pad=dict(
                t=20,
                b=10
            )
        ),
        title_subtitle=dict(
            text=f"{title_report}",
            font=dict(
                size=14,
                color="gray",
                style="italic"
            )
        )
    )

    fig.show()
