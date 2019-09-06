FROM python:3.6

# We have to do this because of: https://github.com/pypa/pipenv/issues/1223
RUN ln -s /usr/local/bin/python /bin/python
RUN pip install 'pipenv==2018.10.9' 

ARG PYPI_USERNAME
ARG PYPI_PASSWORD

WORKDIR /app
ADD Pipfile Pipfile
ADD Pipfile.lock Pipfile.lock
RUN PYPI_USERNAME=$PYPI_USERNAME PYPI_PASSWORD=$PYPI_PASSWORD pipenv sync

ADD .. .

EXPOSE 8000

CMD make run
