from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_KEY: str

    class Config:
        case_sensitive = True


class PostgresSettings(BaseSettings):
    ETL_DB_NAME: str = 'medida_etls'
    ETL_DB_HOST: str = 'postgres_etl'
    ETL_DB_PORT: str = '5432'
    ETL_DB_USER: str = 'medida'
    ETL_DB_PASSWORD: str = 'medida'


class MongoSettings(BaseSettings):
    MONGODB_HOST: str = 'mongo'
    MONGODB_USERNAME: str = 'medida'
    MONGODB_PASSWORD: str = '123456'
    MONGODB_PORT: str = '27017'



@lru_cache()
def get_settings() -> Settings:
    return Settings()
