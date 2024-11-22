FROM python:3.12.2

WORKDIR /app

COPY pyproject.toml ./

RUN pip install poetry
RUN poetry install --no-root --no-dev

COPY src ./src
COPY alembic.ini ./
COPY migrations ./migrations
COPY .env ./

ENV DEBUG=True

EXPOSE 2244

CMD ["bash", "-c", "poetry run alembic upgrade head && poetry run uvicorn src.main:app --host 0.0.0.0 --port 2244"]
