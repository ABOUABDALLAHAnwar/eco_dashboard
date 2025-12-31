FROM python:3.12-slim

# Installer curl et git pour Poetry
RUN apt-get update && apt-get install -y curl git && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY ./data /app/data

WORKDIR /app/backend

# Copier le code du backend
COPY . /app/backend
# Copier pyproject.toml et poetry.lock depuis la racine
COPY ./backend/pyproject.toml ./backend/poetry.lock* ./backend/README.md /app/backend/

# Installer les dépendances via Poetry sans créer de venv
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root


WORKDIR /app

# Lancer FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
