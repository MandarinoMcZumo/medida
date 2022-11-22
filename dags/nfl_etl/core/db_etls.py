from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from nfl_etl.settings.base import PostgresSettings
ps = PostgresSettings()

db_name = ps.ETL_DB_NAME
db_host = ps.ETL_DB_HOST
db_port = ps.ETL_DB_PORT
db_user = ps.ETL_DB_USER
db_pwd = ps.ETL_DB_PASSWORD

url = f"postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"

engine = create_engine(url, pool_size=3, max_overflow=-1, connect_args={'connect_timeout': 500})
Session = sessionmaker(bind=engine)
session = Session()

