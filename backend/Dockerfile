FROM python:3.12-slim

# Installer curl et git pour Poetry
RUN apt-get update && apt-get install -y curl git && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

WORKDIR /app/backend

# Copier pyproject.toml et poetry.lock depuis la racine
COPY ../pyproject.toml ../poetry.lock* /app/
COPY ../README.md /app/README.md
# Installer les dépendances via Poetry sans créer de venv
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Copier le code du backend
COPY . /app/backend

# Lancer FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
