FROM python:3.12


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/lib" \
    VENV_PATH="/opt/.venv"

ENV HOMEDIR="/home/bot"
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt update && apt install --no-install-recommends -y curl build-essential

RUN curl -sSL https://install.python-poetry.org | python3

WORKDIR $HOMEDIR/app

COPY main.py $HOMEDIR/app/main.py
COPY pyproject.toml $HOMEDIR/app/pyproject.toml

RUN poetry install --no-cache

CMD python main.py
