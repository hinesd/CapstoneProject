FROM python:2.7-buster

RUN apt-get update -y

RUN pip install -U pip

RUN mkdir /app

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 80

CMD ["flask","run","--host","0.0.0.0"]
