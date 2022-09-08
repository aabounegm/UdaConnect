from app.udaconnect.services import PersonService

from flask import request
from flask_restx import Namespace, Resource

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa


# TODO: This needs better exception handling


@api.route("/persons")
class PersonsResource(Resource):
    def post(self):
        payload = request.get_json()
        new_person = PersonService.create(payload)
        return new_person

    def get(self):
        persons = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    def get(self, person_id):
        person = PersonService.retrieve(person_id)
        return person
