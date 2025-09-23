import sys
import logging
from decouple import config
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine as ce, MetaData as md
import pandas as pd


logging.basicConfig(
    format = '%(asctime)-5s %(levelname)-8s %(message)s', 
    level=logging.INFO,
    stream=sys.stdout,
    encoding="utf-8"
)


pg_engine = ce(config('ENGINE_PSQL'))


def show_tables():
    conn = pg_engine.connect()
    metadata = md()
    metadata.reflect(bind=conn)
    table_names = metadata.sorted_tables
    logging.info("Estas son las tablas")
    for sheet in table_names:
        print(sheet.name)
    conn.close()
    pg_engine.dispose()
    logging.info("La conexión ha finalizado.")


def query(query: str) -> pd.DataFrame:
    '''
        hacer variable = query(y la consulta sql)
    '''
    try:
        logging.info(f'Aquí está la consulta \n{query}')
        return pd.read_sql_query(sql=query, con=pg_engine)
    except OperationalError:
        logging.error('La conexión se cerró vuelva a conectarlo')
    except Exception as ex:
        logging.error(f'Error durante la conexión: {ex}')
    return pd.DataFrame()


if __name__ == '__main__':
    logging.info("Estoy arrancando...")