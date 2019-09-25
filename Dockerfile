FROM python:3

RUN pip install ansible

ADD . /app

VOLUME /data

WORKDIR /app
ENTRYPOINT ["ansible-playbook", "site.yml"]