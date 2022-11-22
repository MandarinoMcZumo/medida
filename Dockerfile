FROM apache/airflow:2.4.3-python3.9
COPY requirements_etl.txt .
RUN pip install -r requirements_etl.txt