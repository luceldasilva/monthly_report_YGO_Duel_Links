import pandas as pd
import pyprojroot
import datetime


root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'pentaho' / 'output'
sql_path = root_path / 'sql_scripts'
today = datetime.datetime.now().strftime('%d_%m_%Y')


def actualizar_skills():
    df_actualizar = pd.read_excel(
        data_path.joinpath('actualizar_los_dos.xls'),
        sheet_name='actualizar_los_dos'
    )
    sql_file = f'{today}_actualizar_tipo_y_personaje.sql'
    with open(sql_path.joinpath(sql_file), 'w') as file:
        for index, row in df_actualizar.iterrows():
            set_clause = f"skill_type_id = '{row['skill_type_id']}', character_id = '{row['character_id']}'"
            stmt = f"UPDATE skills SET {set_clause} WHERE skill_id = {row['skill_id']};\n"
            file.write(stmt)


def insertar_personajes():
    df_insertar = pd.read_excel(
        data_path.joinpath('characters.xls'),
        sheet_name='characters'
    )
    sql_file = f'{today}_insertar_personajes.sql'
    with open(sql_path.joinpath(sql_file), 'w') as file:
        for index, row in df_insertar.iterrows():
            columnas_sql = 'name_character, serie_id'
            valores_sql = f"'{row['name_character']}', '{row['serie_id']}'"
            stmt = f"INSERT INTO characters ({columnas_sql}) VALUES ({valores_sql});\n"
            file.write(stmt)
