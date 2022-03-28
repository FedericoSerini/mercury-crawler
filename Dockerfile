FROM python:3.8-slim-buster

ADD ./ ./mercury-crawler

RUN pip install Flask
RUN pip install requests

WORKDIR /mercury-crawler

CMD [ "python", "/mercury-crawler/main.py" ]
