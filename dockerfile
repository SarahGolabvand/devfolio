FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
        POETRY_VERSION=2.0.1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /workspace/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml poetry.lock* /workspace/

RUN poetry install --no-interaction --no-ansi --no-root


COPY . /workspace/
EXPOSE 8000
# dev mode
CMD ["python", "app/manage.py", "runserver", "0.0.0.0:8000"]

#production mode
#CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
