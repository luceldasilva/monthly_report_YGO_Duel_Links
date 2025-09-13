import pandas as pd
from visualization import save_plot
from queries_db.constants import comunity_dict
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
import seaborn as sns
from visualization.pie_diagram import comparation_pie_diagram


def venn_graphs(fact_table_df: pd.DataFrame, pivot_comunidad: pd.DataFrame):
    def comunidad(server: str, df: pd.DataFrame=fact_table_df):
        '''
            Para filtrar sus usuarios únicos de cada comunidad
        '''
        df = df[['nick', 'zerotg', 'zephra', 'bryan', 'xenoblur', 'yamiglen', 'latino_vania']]
        return df.query(f'{server} == True')['nick'].drop_duplicates()


    '''
        Gráficos de Venn y de pastel para relaciones
        entre comunidades más grandes
    '''

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

    """
    Comparación de usuarios que están en las comunidades
    """

    count_com = [total, int(nicks_sum - total)]
    labels_com = "Están en\nlas más \nconcurridas", "No están\nen las más\nconcurridas"
    pastel_colors = ['#D291BC', '#BDFCFE']
    title_pie = "Relación de presencia en comunidades"
    fontsize, text_center = 22, 'duelistas'
    
    comparation_pie_diagram(
        count_groupby=count_com,
        labels=labels_com,
        pastel_colors=pastel_colors,
        title_pie=title_pie,
        fontsize=fontsize,
        text_center=text_center
    )


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
    
    save_plot()
    
    plt.show()


    unique_server = size_100 + size_010 + size_001
    two_communities = size_110 + size_101 + size_011

    count_duelists = [unique_server, two_communities, size_111]
    labels = "Una\nsola", "En dos", "Están\nen\nlas 3"
    pastel_colors = ['#92c6ff', '#ffb7ce', '#b7e3cc']
    title_pie = 'De las 3, en cuántas\ncomunidades están'
    fontsize, text_center = 20, 'duelistas'


    comparation_pie_diagram(
        count_groupby=count_duelists,
        labels=labels,
        pastel_colors=pastel_colors,
        title_pie=title_pie,
        fontsize=fontsize,
        text_center=text_center
    )