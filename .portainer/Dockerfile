FROM python:3.8.10-slim

# SETUP POETRY
RUN apt-get update && apt-get install -y curl git
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false

RUN git clone https://github.com/jeremyschiemann/vbox-service-restarter.git
WORKDIR vbox-service-restarter
RUN ls -a
RUN poetry install --no-dev --no-root

CMD python -m app