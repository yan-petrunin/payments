FROM python:3.12.11-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

RUN adduser --disabled-password --no-create-home appuser

COPY src/ ./src/
COPY alembic.ini .

USER appuser

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]