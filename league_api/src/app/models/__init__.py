from pydantic import BaseModel, Field
from typing import Optional


class BaseRequest(BaseModel):
    start_date: str = Field(description='Starting date (YYYY-MM-DD) to retrieve league info.')
    end_date: Optional[str] = Field(
        description='End date (YYYY-MM-DD) to retrieve league info. Defaults to current date or 7 days after the '
                    'start_date.')
    league: Optional[str] = Field(description='League to obtain the results. Defaults to NFL.')
    run_id: Optional[str] = Field(description='Airflow DAG Run ID.')
