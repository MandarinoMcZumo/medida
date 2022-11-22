from datetime import datetime, timedelta
from fastapi import HTTPException
from uuid import uuid4

from ..settings import constants as c
from ..settings.base import get_settings
from ..core.db_mongo import request_collection, ranking_collection, events_collection
from ..log import logger

settings = get_settings()


def ranking_url(league: str = c.LEAGUE) -> str:
    """
    Help function to build the ranking URL with the given parameters
    :param league: League to set as url path in the ranking endpoint
    :return str:
    """
    if not league:
        league = c.LEAGUE
    return f'{c.BASE_URL}{c.RANKING_PATH}/{league}.json?api_key={c.DELIVERY_API_KEY}'


def score_board_url(start_date: str, end_date: str, league: str) -> str:
    """
    Help function to build the score board URL with the given parameters
    :param start_date:
    :param end_date:
    :param league:
    :return:
    """
    if not league:
        league = c.LEAGUE
    return f'{c.BASE_URL}{c.SCORE_BOARD_PATH}/{league}/{start_date}/{end_date}.json?api_key={c.DELIVERY_API_KEY}'


def dates_check(start_date: str, end_date: str = None):
    """

    :param start_date:
    :param end_date:
    :return:
    """
    try:
        sd = datetime.strptime(start_date, '%Y-%m-%d').date()

        if end_date is not None:
            ed = datetime.strptime(end_date, '%Y-%m-%d').date()
        else:
            ed = sd + timedelta(days=7)

        ed = min(datetime.today().date(), ed)

        if sd > ed or sd > datetime.today().date():
            logger.error(f"Invalid dates. start date: {start_date} - end_date: {end_date}")
            raise HTTPException(status_code=400, detail="Invalid dates")

    except Exception as e:
        logger.error(f"Invalid dates. {e}")
        raise e

    return sd.strftime('%Y-%m-%d'), ed.strftime('%Y-%m-%d')


def save_backup(ranking, events, run_id):
    try:
        run_id = run_id if run_id else str(uuid4())
        doc = {'_id': run_id,
               'timestamp': datetime.now(),
               'ranking_request': ranking,
               'events_request': events}
        request_collection.find_one_and_replace({'_id': run_id}, doc, upsert=True)
    except Exception as e:
        logger.error(f"Could not save the request in MongoDB. {e}")


def save_ranking(ranking):
    try:
        ranking_collection.insert_one(ranking)
    except Exception as e:
        logger.error(f'Could not save ranking {ranking.get("_id")}. {e}')


def save_events(events: list):
    for event in events:
        try:
            events_collection.find_one_and_replace({'_id': event.get('event_id')}, event, upsert=True)
        except Exception as e:
            logger.error(f'Could not save event {event.get("event_id")}. {e}')


def get_events(run_id: str, event_calendar: dict):
    events = []
    try:
        for event_day, event_data in event_calendar.items():
            if event_data:
                ed = event_data.get('data')
                for event_id, event_info in ed.items():
                    events.append({
                        '_id': event_id,
                        'run_id': run_id,
                        **event_info
                    })

    except Exception as e:
        logger.error(f'Could not process the events. {e}')

    return events


def get_ranking(run_id: str, ranking_response: dict):
    ranking = {}
    last_update = None
    try:
        last_update = datetime.strptime(ranking_response.get('results', {}).get('last_update'), '%Y-%m-%d %H:%M')
        for team in ranking_response.get('results', {}).get('data'):
            ranking.update({team.get('rank'): team})

    except Exception as e:
        logger.error(f'Could not process ranking data. {e}')

    return {
        'run_id': run_id,
        'timestamp': datetime.now(),
        'last_update': last_update,
        'ranking': ranking
    }
