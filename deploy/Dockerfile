FROM python:3.12-alpine3.20

COPY ./requirements.txt /tmp/
WORKDIR /tmp/
RUN pip install -r requirements.txt && rm requirements.txt

ADD ./terrascope/ /app/terrascope/
WORKDIR /app/terrascope/
ENTRYPOINT ["flask"]
