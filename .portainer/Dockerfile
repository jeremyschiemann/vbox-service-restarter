FROM python:3.8.10-slim

RUN apt-get update && apt-get install -y curl git

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

RUN git clone -b main --single-branch https://github.com/jeremyschiemann/vbox-service-restarter.git

RUN apt-get purge -y curl git

WORKDIR vbox-service-restarter
RUN poetry install --no-dev --no-root
ENTRYPOINT python -m app
