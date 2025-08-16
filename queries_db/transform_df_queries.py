from queries_db.constants import comunidades
import pandas as pd


def pivot_comunity(kog_df: pd.DataFrame):
    melted_comunidad = kog_df.melt(
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

