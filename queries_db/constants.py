from datetime import datetime
import pyprojroot


root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'pentaho' / 'output'
sql_path = root_path / 'sql_scripts'
today = datetime.now().strftime('%d_%m_%Y')
notepad = r'C:\Program Files\Notepad++\notepad++.exe'

comunity_dict: dict = {
    "zerotg": "ZeroTG",
    "zephra": "ZephraCarl",
    "bryan": "Bryan Norén",
    "xenoblur": "Xenoblur",
    "yamiglen": "Yami Glen",
    "latino_vania": "Yam_VT"
}

comunidades: list = [
    'zerotg', 'zephra', 'bryan', 'xenoblur', 'yamiglen', 'latino_vania' 
]

tables_db: list = [
    'kog_2025_jan',
    'kog_2025_feb',
    'kog_2025_mar',
    'kog_2025_abr',
    'kog_2025_may',
    'kog_2025_jun',
    'kog_2025_jul',
    'kog_2025_aug',
    'kog_2025_sep'
]

kc_tables_db: list = [
    'kc_cup_2025_feb',
    'kc_cup_2025_april'
]
