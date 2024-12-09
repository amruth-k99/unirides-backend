from datetime import datetime, timezone
import json
from confluent_kafka import Producer
import socket
topic = 'topic_user_created'


def default_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 format
    return str(obj)


class ProducerRideRequest:
    def __init__(self) -> None:
        conf = {'bootstrap.servers': "localhost:9092",
                'client.id': socket.gethostname()}
        self.producer = Producer(conf)

    # This method will be called inside view for sending Kafka message
    def publish(self, method, body):
        print('Inside RideRequest: Sending to Kafka: ')
        print(body)
        self.producer.produce(
            topic, key="key.ride.requested", value=json.dumps(body, default=default_converter))
