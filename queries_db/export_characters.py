import os
from queries_db import query
from queries_db.constants import data_path
import subprocess


def ver_personajes():
    '''
        Exportar tabla dimensión characters para utilizar en skills
        al asignarles la habilidad a su duelista correspondiente
    '''
    
    name_dim_table = data_path / 'dim_characters.xls'
    
    characters = """
    SELECT name_character, character_id
    FROM characters
    ORDER BY character_id
    """
    
    dim_table = query(characters)
    
    if os.path.exists(name_dim_table):
        os.remove(name_dim_table)
    
    dim_table.to_excel(name_dim_table, sheet_name='characters', index=False)
    subprocess.Popen(f'start "" "{name_dim_table}"', shell=True)
