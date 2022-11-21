import os
import json
from typing import Dict

from kafka import KafkaConsumer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]
KAFKA_URL = os.environ["KAFKA_URL"]
KAFKA_TOPIC = os.environ["KAFKA_TOPIC"]
SQLALCHEMY_DATABASE_URI = (
    f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
Session = sessionmaker(bind=engine)

consumer = KafkaConsumer(KAFKA_TOPIC, bootstrap_servers=[KAFKA_URL])


def save_to_db(location: Dict[str, int]):
    session = Session()

    session.execute(
        "INSERT INTO location (person_id, coordinate)"
        " VALUES (:user_id, ST_Point(:latitude, :longitude))",
        location,
    )
    session.commit()
    session.close()


if __name__ == "__main__":
    for location in consumer:
        message = location.value.decode("utf-8")
        save_to_db(json.loads(message))
