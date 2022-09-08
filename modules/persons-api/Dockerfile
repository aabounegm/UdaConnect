FROM python:3.7-slim-buster

WORKDIR .

# RUN apk add --no-cache gcc musl-dev linux-headers geos libc-dev postgresql-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 5000

COPY . .

RUN python -m grpc_tools.protoc -I ./protos --python_out=. \
           --grpc_python_out=. ./protos/person.proto

CMD ["flask", "run", "--host", "0.0.0.0"]
