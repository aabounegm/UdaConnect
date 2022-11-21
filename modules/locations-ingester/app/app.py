import os
import json
from concurrent import futures

import grpc
from google.protobuf import json_format
from kafka import KafkaProducer

from location_event_pb2 import LocationEvent
import location_event_pb2_grpc

KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]

producer = KafkaProducer(bootstrap_servers=[KAFKA_URL])


class LocationsIngester(location_event_pb2_grpc.LocationIngestorServicer):
    def AddLocation(self, request, context):
        serialized = json_format.MessageToDict(
            request,
            preserving_proto_field_name=True,
        )
        producer.send(KAFKA_TOPIC, json.dumps(serialized))
        return LocationEvent(**serialized)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    location_event_pb2_grpc.add_LocationIngestorServicer_to_server(
        LocationsIngester(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
