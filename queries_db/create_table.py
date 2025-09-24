from queries_db.constants import sql_path, notepad
from datetime import datetime
import subprocess
import textwrap
import locale
import os


def fact_table_init(kc_cup_tournament: bool, rol_user: str):
    
    locale.setlocale(locale.LC_TIME, 'English_United States.1252')
    #* locale.setlocale(locale.LC_TIME, 'en_US.utf8') en Linux/macOS
    
    kc_cup: str = 'kc_cup' if kc_cup_tournament else 'kog'
    
    monthy_table: str = datetime.now().strftime('%Y_%b').lower()
    
    table_name: str = f"{kc_cup}_{monthy_table}"
    
    sql_file = sql_path.joinpath(f'create_{table_name}_fact_table.sql')
    
    if os.path.exists(sql_file):
        raise SystemExit("Archivo ya creado con anterioridad")

    
    script_table: str = textwrap.dedent(f"""\
    CREATE TABLE IF NOT EXISTS {table_name} (
        id SERIAL PRIMARY KEY,
        player_id INT NOT NULL,
        deck_id INT NOT NULL,
        skill_id INT NOT NULL,
        date_id INT NOT NULL,
        zerotg BOOLEAN NOT NULL,
        zephra BOOLEAN NOT NULL,
        bryan BOOLEAN NOT NULL,
        xenoblur BOOLEAN NOT NULL,
        yamiglen BOOLEAN NOT NULL,
        latino_vania BOOLEAN NOT NULL,
        updater_label VARCHAR(32) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW(),
        CONSTRAINT fk_{table_name}_player_id 
            FOREIGN KEY (player_id) 
            REFERENCES players (player_id),
        CONSTRAINT fk_{table_name}_deck_id 
            FOREIGN KEY (deck_id) 
            REFERENCES decks (deck_id),
        CONSTRAINT fk_{table_name}_skill_id
            FOREIGN KEY (skill_id)
            REFERENCES skills (skill_id),
        CONSTRAINT fk_{table_name}_date_id
            FOREIGN KEY (date_id)
            REFERENCES calendar_2025 (date_id)
    );\n
    CREATE TRIGGER trigger_set_updated_at
    BEFORE UPDATE ON {table_name}
    FOR EACH ROW
    EXECUTE FUNCTION set_updated_at();\n
    GRANT SELECT, INSERT, UPDATE, TRUNCATE, REFERENCES, TRIGGER ON {table_name} TO {rol_user};\n
    ALTER TABLE {table_name} OWNER TO {rol_user};
    """)
    
    
    with open(sql_file, 'w') as file:
        file.write(script_table)
    
    subprocess.Popen([notepad, str(sql_file)])
