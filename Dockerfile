FROM python:3.9.0-slim

ENV DOCKER_ENABLED=1

WORKDIR /app

RUN pip install  poetry

COPY . /app

RUN poetry config virtualenvs.create false && poetry install

ENTRYPOINT ["gnakrydev"]

CMD [ "--help" ]