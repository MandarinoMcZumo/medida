from pymongo import MongoClient
import os

client = MongoClient()

MONGODB_DE_HOST = 'localhost'
MONGODB_DE_USERNAME = 'medida'
MONGODB_DE_PASSWORD = '123456'
MONGODB_DE_PORT = '27017'

if os.getenv('MONGODB_DE_HOST') is not None:
    MONGODB_DE_HOST = os.getenv('MONGODB_DE_HOST')

if os.getenv('MONGODB_DE_PASSWORD') is not None:
    MONGODB_DE_PASSWORD = os.getenv('MONGODB_DE_PASSWORD')

if os.getenv('MONGODB_DE_USERNAME') is not None:
    MONGODB_DE_USERNAME = os.getenv('MONGODB_DE_USERNAME')

if os.getenv('MONGODB_DE_PORT') is not None:
    MONGODB_DE_PORT = os.getenv('MONGODB_DE_PORT')


client = MongoClient(f'mongodb://{MONGODB_DE_USERNAME}:{MONGODB_DE_PASSWORD}@{MONGODB_DE_HOST}:{MONGODB_DE_PORT}')
backup_db = client['back_up']
request_collection = backup_db['airflow_requests']

data = client['data']
events_collection = data['events']
ranking_collection = data['ranking']
