import os
import logging
from typing import Dict, List

import grpc
from google.protobuf import json_format
from google.protobuf.empty_pb2 import Empty

from person_pb2_grpc import PersonServiceStub
from person_pb2 import (
    Person,
    PersonRequest,
    People,
)

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("udaconnect-api")

SERVICE_HOST = os.environ["GRPC_HOST"]
SERVICE_PORT = os.environ["GRPC_PORT"]
SERVICE_URL = f"{SERVICE_HOST}:{SERVICE_PORT}"

class PersonService:
    @staticmethod
    def create(person: Dict) -> Dict:
        with grpc.insecure_channel(SERVICE_URL) as channel:
            stub = PersonServiceStub(channel)
            new_person: Person = stub.CreatePerson(json_format.ParseDict(person, Person()))
            return json_format.MessageToDict(new_person, preserving_proto_field_name=True)

    @staticmethod
    def retrieve(person_id: int) -> Dict:
        with grpc.insecure_channel(SERVICE_URL) as channel:
            stub = PersonServiceStub(channel)
            person: Person = stub.GetPerson(PersonRequest(id=person_id))
            return json_format.MessageToDict(person, preserving_proto_field_name=True)

    @staticmethod
    def retrieve_all() -> List[Dict]:
        with grpc.insecure_channel(SERVICE_URL) as channel:
            stub = PersonServiceStub(channel)
            people: People = stub.ListPersons(Empty())
            return [
                json_format.MessageToDict(person, preserving_proto_field_name=True)
                for person in people.persons
            ]
