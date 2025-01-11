from decouple import config
from pymongo import MongoClient


DB_CLIENT = MongoClient(config('ENGINE_CONN')).bankImages

deck_collections = DB_CLIENT.decks

character_collections = DB_CLIENT.characters

CLOUD_NAME = config('CLOUD_NAME')

API_KEY = config('API_KEY')

API_SECRET = config('API_SECRET')