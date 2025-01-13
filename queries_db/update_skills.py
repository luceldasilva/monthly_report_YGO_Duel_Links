from queries_db import pg_engine
from sqlalchemy import MetaData as md, Table, update
import pandas as pd
import pyprojroot


"""
TODO: testear si anda, solucionado el archivo ya lee
"""

root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'pentaho' / 'output'

connection = pg_engine.connect()
metadata = md()
skills = Table('skills', metadata, autoload_with=connection)


df = pd.read_excel(
    data_path.joinpath('actualizar_los_dos.xls'),
    sheet_name='actualizar_los_dos'
)

for index, row in df.iterrows():
    stmt = (
        update(skills).
        where(skills.c.skill_id == row['skill_id']).
        values(
            skill_type_id=row['skill_type_id'],
            character_id=row['character_id']
        )
    )
    connection.execute(stmt)


connection.close()
