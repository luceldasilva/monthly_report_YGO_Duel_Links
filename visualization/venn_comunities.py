import pandas as pd
from visualization import save_plot
from queries_db.constants import comunity_dict
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from matplotlib_venn import venn2
import seaborn as sns
from visualization.pie_diagram import comparation_pie_diagram


def venn_graphs(
    save_photo: bool,
    fact_table_df: pd.DataFrame,
    pivot_comunidad: pd.DataFrame,
    comparation_bool: bool = False,
    venn_bool: bool = True,
    population_bool: bool = False
):
    """
    Gráficos de Venn y de pastel para relaciones
    entre comunidades más grandes

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    fact_table_df : pandas.DataFrame
        Tabla de hechos a estudiar
    pivot_comunidad : pd.DataFrame
        _description_
    comparation_bool : bool, optional
        Comparación de usuarios que están en las comunidades,
        por defecto es False
    venn_bool : bool, optional
        Gráfico de Venn entre las 3 comunidades con más registros,
        por defecto es True
    population_bool : bool, optional
        Comparativa en ver si entre las 3 comunidades más si están en las 3,
        por defecto es False
    """
    def comunidad(server: str, df: pd.DataFrame=fact_table_df):
        '''
            Para filtrar sus usuarios únicos de cada comunidad
        '''
        df = df[['nick', 'zerotg', 'zephra', 'bryan', 'xenoblur', 'yamiglen', 'latino_vania']]
        return df.query(f'{server} == True')['nick'].drop_duplicates()


    comunidad_list_top_three = pivot_comunidad.index[:3]

    comunity_top_one = comunidad(comunidad_list_top_three[0])
    comunity_top_two = comunidad(comunidad_list_top_three[1])
    comunity_top_three = comunidad(comunidad_list_top_three[2])

    set_top_one = set(comunity_top_one)
    set_top_two = set(comunity_top_two)
    set_top_three = set(comunity_top_three)

    size_100 = len(set_top_one - (set_top_two | set_top_three))
    size_010 = len(set_top_two - (set_top_one | set_top_three))
    size_001 = len(set_top_three - (set_top_one | set_top_two))
    size_110 = len((set_top_one & set_top_two) - set_top_three)
    size_101 = len((set_top_one & set_top_three) - set_top_two)
    size_011 = len((set_top_two & set_top_three) - set_top_one)
    size_111 = len(set_top_one & set_top_two & set_top_three)

    total = sum(
        [size_100, size_010, size_001, size_110, size_101, size_011, size_111]
    )

    nicks_sum: int = int(fact_table_df.nick.drop_duplicates().count())

    percent_100 = (size_100 / nicks_sum) * 100
    percent_010 = (size_010 / nicks_sum) * 100
    percent_001 = (size_001 / nicks_sum) * 100
    percent_110 = (size_110 / nicks_sum) * 100
    percent_101 = (size_101 / nicks_sum) * 100
    percent_011 = (size_011 / nicks_sum) * 100
    percent_111 = (size_111 / nicks_sum) * 100

    if comparation_bool:
        count_com = [total, int(nicks_sum - total)]
        labels_com = "Están en\nlas más \nconcurridas", "No están\nen las más\nconcurridas"
        pastel_colors = ['#D291BC', '#BDFCFE']
        title_pie = "Relación de presencia en comunidades"
        fontsize, text_center = 22, 'duelistas'
        
        comparation_pie_diagram(
            save_photo=save_photo,
            count_groupby=count_com,
            labels=labels_com,
            pastel_colors=pastel_colors,
            title_pie=title_pie,
            fontsize=fontsize,
            text_center=text_center
        )
    

    if venn_bool:
        fig, ax = plt.subplots(figsize=(10, 8))

        venn = venn3(
            [set_top_one, set_top_two, set_top_three],
            set_labels=(
                comunity_dict[comunidad_list_top_three[0]],
                comunity_dict[comunidad_list_top_three[1]],
                comunity_dict[comunidad_list_top_three[2]]
            )
        )

        venn.get_label_by_id('100').set_text(
            f"{size_100}\n{percent_100:.2f}%")
        venn.get_label_by_id('010').set_text(
            f"{size_010}\n{percent_010:.2f}%")
        venn.get_label_by_id('001').set_text(
            f"{size_001}\n{percent_001:.2f}%")
        venn.get_label_by_id('110').set_text(
            f"{size_110}\n{percent_110:.2f}%")
        venn.get_label_by_id('101').set_text(
            f"{size_101}\n{percent_101:.2f}%")
        venn.get_label_by_id('011').set_text(
            f"{size_011}\n{percent_011:.2f}%")
        venn.get_label_by_id('111').set_text(
            f"{size_111}\n{percent_111:.2f}%")


        colors = sns.color_palette('Set3', 7)
        for patch, color in zip(venn.patches, colors):
            patch.set_facecolor(color)


        for label in venn.set_labels:
            label.set_fontsize(20)

        for label in venn.subset_labels:
            if label:
                label.set_fontsize(16)

        ax.set_title(
            'Gráfico de Venn',
            fontsize=28,
            fontweight="bold"
        )
        
        if save_photo:
            save_plot()
        
        plt.show()
    
    
    if population_bool:
        unique_server = size_100 + size_010 + size_001
        two_communities = size_110 + size_101 + size_011

        count_duelists = [unique_server, two_communities, size_111]
        labels = "Una\nsola", "En dos", "Están\nen\nlas 3"
        pastel_colors = ['#92c6ff', '#ffb7ce', '#b7e3cc']
        title_pie = 'De las 3, en cuántas\ncomunidades están'
        fontsize, text_center = 20, 'duelistas'


        comparation_pie_diagram(
            save_photo=save_photo,
            count_groupby=count_duelists,
            labels=labels,
            pastel_colors=pastel_colors,
            title_pie=title_pie,
            fontsize=fontsize,
            text_center=text_center
        )


def compare_with_kc_cup(
    save_photo: bool,
    kog_df: pd.DataFrame,
    kc_df: pd.DataFrame,
    month_fact_table: str,
    year_fact_table: str
):
    """
    Diagrama de Venn para mostrar cuantos usuarios en el mismo mes
    llegaron a KOG y al DLv. MAX

    Parameters
    ----------
    save_photo : bool
        Guardar la imagen
    kog_df : pd.DataFrame
        Tabla de hechos referende a KOG
    kc_df : pd.DataFrame
        Tabla de hechos referende a la Copa KC
    month_fact_table : str
        Mes correspondiente a `kog_df` y `kc_df`
    year_fact_table : str
        Año correspondiente a `kog_df` y `kc_df`
    """
    kc_users = set(kc_df.nick.drop_duplicates())
    kog_users = set(kog_df.nick.drop_duplicates())

    solo_kc = len(kc_users - kog_users)
    solo_kog = len(kog_users - kc_users)
    interseccion = len(kc_users & kog_users)

    plt.figure(figsize=(5,5))

    venn2(
        subsets=(
            solo_kc, solo_kog, interseccion
        ),
        set_colors=(
            "cyan",
            "gold"
        ),
        set_labels=(
            'LLegaron a DLv. MAX',
            'Llegaron a KOG'
        )
    )

    plt.title(
        f"Diagrama de Venn de Usuarios\nen {month_fact_table} {year_fact_table}",
        fontsize=14,
        fontweight='bold'
    )
    
    if save_photo:
        save_plot()
    
    plt.show()