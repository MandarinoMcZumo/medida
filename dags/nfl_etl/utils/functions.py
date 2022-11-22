import pandas as pd
import json

from nfl_etl.core.db_mongo import events_collection, ranking_collection
from nfl_etl.core.db_etls import engine
from nfl_etl.log import logger


def fetch_events(run_id: str) -> list:
    """
    Gets the events stored in Mongo DB for the given run_id.
    :param str run_id: Airflow unique run id
    :return: list of events with the necessary fields to build the dashboard.
    """
    events = []
    try:
        event_fields = {
            'event_id': 1,
            'event_date': 1,
            'away_team_id': 1,
            'away_nick_name': 1,
            'away_city': 1,
            'home_team_id': 1,
            'home_nick_name': 1,
            'home_city': 1,
        }
        all_events = events_collection.find({'run_id': run_id}, event_fields)
        events = [event for event in all_events]

    except Exception as e:
        logger.error(f'Could not get the events. {e}')

    return events


def fetch_ranking(run_id: str) -> dict:
    """
    Gets the ranking stored in Mongo DB for the given run_id.
    :param str run_id: Airflow unique run id
    :return: dict of rank positions
    """
    ranking = []
    try:
        full_ranking = ranking_collection.find({'run_id': run_id}, {'ranking': 1})
        ranking = [rank for rank in full_ranking][0].get('ranking')
    except Exception as e:
        logger.error(f'Could not get the ranking. {e}')

    return ranking


def build_ranking_df(ranking: dict) -> pd.DataFrame:
    """
    Builds the ranking Dataframe and selects the necessary columns
    :param dict ranking:
    :return:
    """
    ranking = pd.DataFrame(ranking).T
    return ranking[['team_id', 'rank', 'adjusted_points']]


def build_events_df(events: list) -> pd.DataFrame:
    """
    Builds the events Dataframe
    :param list events:
    :return:
    """
    return pd.DataFrame(events)


def build_dashboard(events: pd.DataFrame, ranking: pd.DataFrame) -> pd.DataFrame:
    """
    Merges events and rankings, applying the mandatory data types and formats and generating the new event_time, event_date
    and rank_points columns.
    :param list events:
    :param dict ranking:
    :return:
    """
    events['event_time'] = events['event_date'].astype('datetime64').dt.strftime('%H:%M')
    events['event_date'] = events['event_date'].astype('datetime64').dt.strftime('%Y-%m-%d')
    ranking['rank_points'] = ranking['adjusted_points'].astype('float64').round(2)
    ranking.drop(columns=['adjusted_points'], inplace=True)
    df = events \
        .merge(ranking.add_prefix('home_'), left_on='home_team_id', right_on='home_team_id') \
        .merge(ranking.add_prefix('away_'), left_on='away_team_id', right_on='away_team_id')
    return df


def update_dashboard(new_dashboard: pd.DataFrame):
    """
    Iterates through the merged data and updates the final Postgres dashboard
    :param new_dashboard:
    :return:
    """
    with engine.connect() as conn:
        for i, row in new_dashboard.iterrows():
            try:
                query = build_query(row)
                conn.execute(query)
            except Exception as e:
                logger.error(f'Could not update the dashboard for event {row.event_id}. {e}')


def build_query(row: pd.Series) -> str:
    """
    Builds the UPSERT query by updating on conflict with the event_id index constraint
    :param row:
    :return:
    """
    insert_query = 'SELECT 1'
    try:
        insert_query = f"""
        INSERT INTO events_nfl (event_id, event_date, event_time, away_team_id, away_nick_name, away_city, 
                            away_rank, away_rank_points, home_team_id, home_nick_name, home_city, home_rank, home_rank_points)
                            VALUES (
                            '{row.event_id}', '{row.event_date}', '{row.event_time}', 
                            '{row.away_team_id}', '{row.away_nick_name}', '{row.away_city}', 
                            {row.away_rank}, {row.away_rank_points}, '{row.home_team_id}', 
                            '{row.home_nick_name}', '{row.home_city}', {row.home_rank}, {row.home_rank_points})
        ON CONFLICT ON CONSTRAINT events_nfl_pkey
            DO
        UPDATE SET event_date = '{row.event_date}',
                   event_time = '{row.event_time}',
                   away_team_id = '{row.away_team_id}',
                   away_nick_name = '{row.away_nick_name}',
                   away_city = '{row.away_city}',
                   away_rank = {row.away_rank},
                   away_rank_points = {row.away_rank_points},
                   home_team_id = '{row.home_team_id}',
                   home_nick_name = '{row.home_nick_name}',
                   home_city = '{row.home_city}',
                   home_rank = {row.home_rank},
                   home_rank_points = {row.home_rank_points};"""
    except Exception as e:
        logger.error(f'Could not build the query. {e}')

    return insert_query
