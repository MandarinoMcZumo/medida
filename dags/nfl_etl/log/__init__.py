import logging
from logging.config import dictConfig

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s.%(msecs)d]-[%(name)s]-[%(levelname)s]-%(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
})

logger = logging.getLogger("airflow.task")
