FROM python:3.10
RUN pip install poetry
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
COPY . /code
CMD python manage.py

FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN pip3 install poetry
RUN poetry install