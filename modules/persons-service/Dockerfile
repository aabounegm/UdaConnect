FROM python:3.7-slim-buster

WORKDIR /service

COPY requirements.txt requirements.txt

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

COPY protos/ /service/protos/

COPY app/ /service/app

RUN python -m grpc_tools.protoc -I ./protos --python_out=./app \
           --grpc_python_out=./app ./protos/person.proto


EXPOSE 50051

ENTRYPOINT [ "python", "app/app.py" ]
