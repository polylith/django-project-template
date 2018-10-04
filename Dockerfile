FROM python:3.6-onbuild

RUN apt-get update
RUN apt-get install -y postgresql-client

# We have to do this because of: https://github.com/pypa/pipenv/issues/1223
RUN ln -s /usr/local/bin/python /bin/python

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

RUN PYPI_USERNAME=$PYPI_USERNAME PYPI_PASSWORD=$PYPI_PASSWORD pipenv lock --requirements > requirements.txt
RUN pip install -q -r requirements.txt

EXPOSE 8000

CMD make run
