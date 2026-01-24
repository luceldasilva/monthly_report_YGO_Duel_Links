from datetime import datetime
from decouple import config
import pyprojroot


root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'output'
sql_path = root_path / 'sql_scripts'
today = datetime.now().strftime('%d_%m_%Y')
notepad = r'C:\Program Files\Notepad++\notepad++.exe'

comunity_dict: dict[str, str] = {
    "zerotg": "ZeroTG",
    "zephra": "ZephraCarl",
    "bryan": "Bryan Norén",
    "xenoblur": "Xenoblur",
    "yamiglen": "Yami Glen",
    "latino_vania": "Yam_VT"
}

comunidades: list[str] = [
    'zerotg', 'zephra', 'bryan', 'xenoblur', 'yamiglen', 'latino_vania' 
]

avatars: list[str] = [
    config('ZEROTG'),
    config('ZEPHRA'),
    config('BRYAN'),
    config('XENOBLUR'),
    config('YAMIGLEN'),
    config('YAM_VT'),
]

db_2025_tables: list[str] = [
    'kog_2025_jan',
    'kog_2025_feb',
    'kog_2025_mar',
    'kog_2025_abr',
    'kog_2025_may',
    'kog_2025_jun',
    'kog_2025_jul',
    'kog_2025_aug',
    'kog_2025_sep',
    'kog_2025_oct',
    'kog_2025_nov',
    'kog_2025_dec'
]

tables_db: list[str] = [
    'kog_2025_dec',
    'kog_2026_jan'
]

kc_tables_db: list[str] = [
    'kc_cup_2025_feb',
    'kc_cup_2025_april',
    'kc_cup_2025_sep',
    'kc_cup_2025_nov'
]


def get_tables_by_year(year: int) -> list[str]:
    """
    Traer la lista de las tablas del año correspondiente

    Parameters
    ----------
    year : int
        Año en Cuestión

    Returns
    -------
    list[str]
        La lista de las tablas de ese año
    """
    TABLES_BY_YEAR: dict[int, list[str]] = {
        2025: db_2025_tables,
        2026: tables_db[1:],
    }

    return list(TABLES_BY_YEAR.get(year, []))
