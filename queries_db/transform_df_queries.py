from queries_db.constants import comunidades, data_path
import pandas as pd
import rpy2.robjects as ro
from rpy2.robjects.conversion import localconverter
from rpy2.robjects import pandas2ri
from rpy2.robjects import RObject
import os


def pivot_comunity(fact_df: pd.DataFrame):
    melted_comunidad = fact_df.melt(
        id_vars='nick',
        value_vars=comunidades, 
        var_name='Comunidad', value_name='Jugadores'
    )

    pivot_comunidad = pd.pivot_table(
        melted_comunidad,
        values='Jugadores',
        index='Comunidad',
        aggfunc=lambda x: (x == True).sum()
    ).sort_values(by='Jugadores', ascending=False)
    
    return pivot_comunidad


def decks_with_avatar(decks_sum: pd.DataFrame, limit: int):
    
    decks_images = pd.read_json(
        'https://monthly-report-yugioh-dl.vercel.app/decks/',
        orient='records'
    )

    decks_images = decks_images[['name', 'url_image']]

    decks_with_avatar_df = decks_sum.iloc[:limit]
    decks_with_avatar_df = decks_with_avatar_df.merge(
        decks_images, on='name', how='inner'
    )
    decks_with_avatar_df.rename(columns={'name': 'deck'}, inplace=True)
    
    return decks_with_avatar_df


def converter_to_r(df: pd.DataFrame, name_file: str):
    with localconverter(ro.default_converter + pandas2ri.converter):
        r_df: RObject = ro.conversion.py2rpy(df)
        
    df_name = f'{name_file}.rds'
    
    df_file = data_path.joinpath(df_name)
    
    if os.path.exists(df_file):
        os.remove(df_file)
    
    ro.r.assign("r_df", r_df)
    ro.r(f'saveRDS(r_df, file = "{df_file.as_posix()}")')

