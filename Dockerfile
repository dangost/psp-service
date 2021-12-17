FROM python:3.9


WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY src/  /app/src

RUN pip install poetry &&\
    poetry config virtualenvs.create false &&\
    poetry install

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "src.app:create_app()"]

EXPOSE 8080
