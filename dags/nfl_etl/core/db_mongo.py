from nfl_etl.settings.base import MongoSettings
from pymongo import MongoClient

ms = MongoSettings()

client = MongoClient()


client = MongoClient(f'mongodb://{ms.MONGODB_USERNAME}:{ms.MONGODB_PASSWORD}@{ms.MONGODB_HOST}:{ms.MONGODB_PORT}')
backup_db = client['back_up']
request_collection = backup_db['airflow_requests']

data = client['data']
events_collection = data['events']
ranking_collection = data['ranking']
