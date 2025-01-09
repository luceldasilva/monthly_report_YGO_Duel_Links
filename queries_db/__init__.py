import logging
from decouple import config
from sqlalchemy import create_engine as ce, MetaData as md
import pandas as pd


logging.basicConfig(
    format = '%(asctime)-5s %(levelname)-8s %(message)s', 
    level=logging.INFO,  
    encoding="utf-8"
)


pg_engine = ce(config('ENGINE_PSQL'))


def show_tables():
	conn = pg_engine.connect()
	metadata = md()
	metadata.reflect(bind=conn)
	table_names = metadata.sorted_tables
	for sheet in table_names:
		logging.info(sheet.name)
	conn.close()
	pg_engine.dispose()
	logging.info("La conexión ha finalizado.")


def query(query):
	'''
		hacer variable = query(y la consulta sql)
	'''
	try:
		return pd.read_sql_query(sql=query, con=pg_engine)
	except Exception as ex:
		logging.error(f'Error durante la conexión: {ex}')
	finally:
		logging.info(f'Aquí está la consulta \n{query}')


if __name__ == '__main__':
	logging.info("Estoy arrancando...")