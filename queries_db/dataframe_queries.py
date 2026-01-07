import pandas as pd
from datetime import date
from queries_db import query as qu


def df_query(
    fact_table: str, alias_fact_table: str, year: str
) -> pd.DataFrame:
    """
    Tabla de hechos del mes/copa KC a estudiar
    
    Parameters
    ----------
    fact_table : str
        Nombre de la tabla de hechos
    alias_fact_table : str
        Abreviatura de `fact_table` para las consultas sql
    
    Returns
    -------
    pandas.DataFrame
    """
    fact_query = f"""
    SELECT 
        p.nick, d.deck, s.skill, c.ndmax,
        {alias_fact_table}.zerotg, {alias_fact_table}.zephra,
        {alias_fact_table}.bryan, {alias_fact_table}.xenoblur,
        {alias_fact_table}.yamiglen, {alias_fact_table}.latino_vania
    FROM {fact_table} {alias_fact_table}
    INNER JOIN decks d ON {alias_fact_table}.deck_id = d.deck_id
    INNER JOIN players p ON {alias_fact_table}.player_id = p.player_id
    INNER JOIN skills s ON {alias_fact_table}.skill_id = s.skill_id
    INNER JOIN calendar_{year} c ON {alias_fact_table}.date_id = c.date_id;
    """

    fact_df = qu(fact_query)
    return fact_df


def date_df(
    fact_table: str,
    alias_fact_table: str,
    date_fact_table: date
) -> pd.DataFrame:
    """
    Tabla de los días del mes y sus registros correspondientes
    
    Parameters
    ----------
    fact_table : str
    alias_fact_table : str
    date_fact_table : datetime.date
    
    Returns
    -------
    pandas.DataFrame
    """
    date_query = f"""
    SELECT 
        c.day_of_monthy, 
        COALESCE(COUNT({alias_fact_table}.date_id), 0) AS jugadores
    FROM calendar_{date_fact_table.year} c
    LEFT JOIN {fact_table} {alias_fact_table} 
        ON {alias_fact_table}.date_id = c.date_id
    WHERE c.monthy = {date_fact_table.month}
    GROUP BY c.day_of_monthy
    ORDER BY c.day_of_monthy;
    """

    date_df = qu(date_query)
    return date_df


def decks_df(fact_table: str, alias_fact_table: str) -> pd.DataFrame:
    """
    Lista de mazos con sus registros correspondientes
    
    Parameters
    ----------
    fact_table : str
        Tabla de hechos a estudiar
    alias_fact_table : str
        Abreviatura de `fact_table` para las consultas sql
    
    Returns
    -------
    pandas.DataFrame
    """
    decks_count_query = f"""
    SELECT
        d.deck AS name, COUNT(*) AS total
    FROM {fact_table} {alias_fact_table}
    INNER JOIN decks d ON {alias_fact_table}.deck_id = d.deck_id
    GROUP BY name
    ORDER BY total DESC;
    """

    decks_sum = qu(decks_count_query)
    return decks_sum
