from datetime import datetime
import pyprojroot


root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'pentaho' / 'output'
sql_path = root_path / 'sql_scripts'
today = datetime.now().strftime('%d_%m_%Y')
notepad = r'C:\Program Files\Notepad++\notepad++.exe'