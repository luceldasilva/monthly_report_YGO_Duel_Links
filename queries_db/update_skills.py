from queries_db.constants import data_path, sql_path, today, notepad
import pandas as pd
import subprocess


def actualizar_skills(kc_cup_tournament: bool = False):
    """
    Actualizar habilidades con su personaje correspondiente si lo tiene

    Parameters
    ----------
    kc_cup_tournament : bool
        Usar kc_cup_tournament para actualizar datos de copa kc
    """


    kc_cup = 'kc_cup_' if kc_cup_tournament else ''
    
    df_actualizar = pd.read_excel(
        data_path.joinpath(f'{kc_cup}actualizar_los_dos.xls'),
        sheet_name='actualizar_los_dos'
    )
    df_actualizar.dropna(inplace=True)
    sql_file = sql_path.joinpath(f'{today}_{kc_cup}actualizar_tipo_y_personaje.sql')
    with open(sql_file, 'w') as file:
        for index, row in df_actualizar.iterrows():
            set_clause = f"skill_type_id = {int(row['skill_type_id'])}, character_id = {int(row['character_id'])}"
            stmt = f"UPDATE skills SET {set_clause} WHERE skill_id = {int(row['skill_id'])};\n"
            file.write(stmt)
    
    subprocess.Popen([notepad, str(sql_file)])
    


def insertar_personajes(kc_cup_tournament: bool = False):
    """
    Insertar personajes para cargar a la base de datos

    Parameters
    ----------
    kc_cup_tournament : bool
        Usar kc_cup_tournament para actualizar datos de copa kc
    """


    kc_cup = 'kc_cup_' if kc_cup_tournament else ''


    df_insertar = pd.read_excel(
        data_path.joinpath(f'{kc_cup}characters.xls'),
        sheet_name='characters'
    )
    df_insertar.dropna(inplace=True)
    sql_file = sql_path.joinpath(f'{today}_{kc_cup}insertar_personajes.sql')
    with open(sql_file, 'w') as file:
        for index, row in df_insertar.iterrows():
            columnas_sql = 'name_character, serie_id'
            name_character = str(row['name_character'])
            serie_id = int(row['serie_id'])
            stmt = f"INSERT INTO characters ({columnas_sql}) VALUES {name_character, serie_id};\n"
            file.write(stmt)
    
    subprocess.Popen([notepad, str(sql_file)])
    
