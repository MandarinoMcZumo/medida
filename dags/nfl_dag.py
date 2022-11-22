from airflow.decorators import dag, task
from datetime import datetime, timedelta
from uuid import uuid4
import requests
import json

from nfl_etl.main import execute_etl

START_DATE = datetime.today() - timedelta(days=7)
default_args = {
    'start_date': START_DATE,
    'concurrency': 1
}

@dag('NFL_Dashboard', schedule_interval='@hourly', default_args=default_args, catchup=False)
def taskflow():

    @task
    def call_league_api():
        custom_run_uuid = str(uuid4())
        url = 'http://league_api:80/fetch/'
        payload = json.dumps({'start_date': START_DATE.strftime('%Y-%m-%d'), 'run_id': custom_run_uuid})
        headers = {
            'Authorization': 'Bearer 123456',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return {'custom_run_id': custom_run_uuid}

    @task
    def nfl_etl(custom_run_uuid: str):
        """
        Gets totalTestResultsIncrease field from Covid API for given state and returns value
        """
        execute_etl(custom_run_uuid['custom_run_id'])
        return {'received_custom_run_id': custom_run_uuid['custom_run_id']}

    nfl_etl(call_league_api())

dag = taskflow()