from queries_db.constants import root_path, data_path, today, notepad
import pandas as pd
import subprocess
import json


def json_decks(kc_cup_tournament: bool = False, pentaho: bool = False):
    """
    Cargar el avatar de los mazos a la base de datos de MongoDB

    Parameters
    ----------
    kc_cup_tournament : bool
        Usar kc_cup_tournament para actualizar datos de copa kc
    """


    kc_cup = 'kc_cup_' if kc_cup_tournament else ''

    path_excel = root_path / 'etl' /  'pentaho' / 'output' if pentaho else data_path


    df_decks = pd.read_excel(
        path_excel.joinpath(f'{kc_cup}upload_avatar_decks.xls'),
        sheet_name='decks'
    )
    df_decks.dropna(inplace=True)
    json_file = path_excel.joinpath(f'{today}_{kc_cup}upload_avatar_decks.json')
    
    with open(json_file, 'w') as file:
        for _, row in df_decks.iterrows():
            row_dict = row.to_dict()
            json_str = json.dumps(row_dict, indent=2, ensure_ascii=False)
            file.write(json_str + "\n")
    
    subprocess.Popen([notepad, str(json_file)])
    
