from queries_db.constants import data_path, today, notepad
import pandas as pd
import subprocess


def json_decks():
    df_decks = pd.read_excel(
        data_path.joinpath('upload_avatar_decks.xls'),
        sheet_name='decks'
    )
    df_decks.dropna(inplace=True)
    json_file = data_path.joinpath(f'{today}_upload_avatar_decks.json')
    
    with open(json_file, 'w') as file:
        for _, row in df_decks.iterrows():
            json_str = row.to_json(indent=4, force_ascii=False)
            formatted_json = json_str.replace(':', ': ')
            file.write(formatted_json + "\n")
    
    subprocess.Popen([notepad, str(json_file)])
