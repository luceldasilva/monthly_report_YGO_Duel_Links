from queries_db import pg_engine
from sqlalchemy import MetaData as md, Table, update
import pandas as pd
import pyprojroot


"""
TODO: corregir el df no anda y no lee, a lo sumo cambiar el tipo de archivo :v
"""

root_path = pyprojroot.here()
data_path = root_path / 'etl' / 'pentaho' / 'output'

connection = pg_engine.connect()
metadata = md()
skills = Table('skills', metadata, autoload_with=connection)


df = pd.read_csv(data_path.joinpath('actualizar_los_dos.csv'))

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
