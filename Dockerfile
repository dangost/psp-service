FROM python:3.9


WORKDIR /app
COPY pyproject.toml poetry.lock .env entrypoint.sh /app/
COPY src/  /app/src

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "-m", "src"]

EXPOSE 5000