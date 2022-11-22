from uuid import uuid4
from datetime import datetime, timedelta
import requests
import json
from nfl_etl.utils.functions import fetch_events, fetch_ranking, build_ranking_df, build_events_df, build_dashboard, \
    update_dashboard, call_external_api
from nfl_etl.log import logger

def execute_etl(custom_run_uuid):
    logger.info(f'New request with run id {custom_run_uuid}')
    events = fetch_events(custom_run_uuid)
    events_df = build_events_df(events)
    ranking = fetch_ranking(custom_run_uuid)
    ranking_df = build_ranking_df(ranking)
    dashboard = build_dashboard(events_df, ranking_df)
    update_dashboard(dashboard)
    logger.info(f'Request {custom_run_uuid} finished succesfully!')
