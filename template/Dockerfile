FROM python:3.7

RUN ln -s /usr/local/bin/python /bin/python
RUN pip install poetry

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

WORKDIR /app
ADD pyproject.toml pyproject.toml
ADD poetry.lock poetry.lock
RUN POETRY_HTTP_BASIC_ENTWICKLERHELD_USERNAME=$PYPI_USERNAME POETRY_HTTP_BASIC_ENTWICKLERHELD_PASSWORD=$PYPI_PASSWORD poetry install

ADD . .

EXPOSE 8000

CMD make run
