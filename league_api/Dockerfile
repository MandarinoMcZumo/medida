FROM python:3.9.1-slim

ENV HOMEDIR=/app/ TERM=vt100 C_FORCE_RROT=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app

WORKDIR ${HOMEDIR}

RUN apt-get update -y --fix-missing && apt-get install -y git=*

RUN pip install --no-cache-dir --upgrade pip==22.2.2 poetry==1.2.1 supervisor==4.2.1 && \
    poetry config virtualenvs.create false

COPY src/pyproject.toml $HOMEDIR/pyproject.toml
COPY src/poetry.lock $HOMEDIR/poetry.lock

RUN poetry install

COPY src ${HOMEDIR}

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
