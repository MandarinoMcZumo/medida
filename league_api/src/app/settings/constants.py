import os

BASE_URL = 'https://delivery.chalk247.com/'

RANKING_PATH = 'team_rankings'
SCORE_BOARD_PATH = 'scoreboard'
LEAGUE = 'NFL'

DELIVERY_API_KEY = '74db8efa2a6db279393b433d97c2bc843f8e32b0'
API_KEY = '123456'
if os.getenv('API_KEY') is not None:
    API_KEY = os.getenv('API_KEY')

SENTRY_DSN = 'https://cdc8d308964a4864935620b5ee7b4d9a@o4504191572180992.ingest.sentry.io/4504191573688321'
if os.getenv('SENTRY_DSN') is not None:
    SENTRY_DSN = os.getenv('SENTRY_DSN')



