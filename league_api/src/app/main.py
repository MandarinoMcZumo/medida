from fastapi import FastAPI, Security, HTTPException
import requests
import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from uuid import uuid4

from .settings.base import get_settings
from .settings import security
from .models import BaseRequest
from .log import logger
from .utils.functions import dates_check, ranking_url, score_board_url, get_events, get_ranking, save_backup, \
    save_events, save_ranking

settings = get_settings()

sentry_sdk.init(
    dsn="https://cdc8d308964a4864935620b5ee7b4d9a@o4504191572180992.ingest.sentry.io/4504191573688321",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)

app = FastAPI()


@app.on_event('startup')
async def startup_event():
    global app
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN
    )
    app = SentryAsgiMiddleware(app)


@app.get('/')
async def ping():
    return 'PONG'


@app.post('/fetch/', dependencies=[Security(security.api_key_auth)])
async def fetch_data(base_request: BaseRequest):
    """
    Main API Endpoint.
    Validates the given date/dates
    Fetches the external info
    Backs up the raw data
    Creates and saves the Mongo DB documents
    """
    success = True
    run_id = base_request.run_id if base_request.run_id else str(uuid4())
    logger.info('New fetch request.')
    try:
        start_date, end_date = dates_check(base_request.start_date, base_request.end_date)

        logger.debug('Fetching data...')
        ranking_response = requests.get(ranking_url(base_request.league))
        score_board_response = requests.get(score_board_url(start_date, end_date, base_request.league))

        if ranking_response.status_code != 200 or score_board_response.status_code != 200:
            raise HTTPException(status_code=503, detail="External data provider is not available.")

        ranking = ranking_response.json()
        score_board = score_board_response.json()

        logger.debug('Verifying data...')
        events_doc = get_events(run_id, score_board.get('results'))
        ranking_doc = get_ranking(run_id, ranking)

        logger.debug('Saving data...')
        save_backup(ranking, score_board, base_request.run_id)
        save_events(events_doc)
        save_ranking(ranking_doc)
        logger.debug('Data successfully saved!')
        logger.info('Fetch request was completed successfully!')

    except Exception as e:
        logger.error(f'Could not fetch the data. {e}')
        success = False

    return {'success': success}
