FROM python:3.7-slim-buster

WORKDIR /consumer

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY app/ /consumer/app

ENTRYPOINT [ "python", "app/app.py" ]
