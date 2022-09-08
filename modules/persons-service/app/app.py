import os
from concurrent import futures

import grpc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from person_pb2 import Person as PersonProto, People
import person_pb2_grpc
from models import Person, Base

DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class PersonsService(person_pb2_grpc.PersonServiceServicer):
    def GetPerson(self, request, context):
        session = Session()
        person: Person = session.get(Person, request.person_id)
        session.close()
        if person is None:
            context.abort(grpc.StatusCode.NOT_FOUND, "Person not found")

        return PersonProto(id=person.id,
                      first_name=person.first_name,
                      last_name=person.last_name,
                      company_name=person.company_name)

    def CreatePerson(self, request, context):
        session = Session()
        person = Person(first_name=request.first_name,
                                last_name=request.last_name,
                                company_name=request.company_name)
        session.add(person)
        session.commit()
        session.close()
        return PersonProto(id=person.id,
                      first_name=person.first_name,
                      last_name=person.last_name,
                      company_name=person.company_name)

    def ListPersons(self, request, context):
        session = Session()
        persons = session.query(Person).all()
        session.close()
        people = People()
        people.persons.extend([
            PersonProto(id=person.id,
                      first_name=person.first_name,
                      last_name=person.last_name,
                      company_name=person.company_name)
            for person in persons
        ])
        return people


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    person_pb2_grpc.add_PersonServiceServicer_to_server(
        PersonsService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
