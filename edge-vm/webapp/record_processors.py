import dataclasses
import json
import socket
from typing import Dict, Any
import flask
from confluent_kafka import Producer

from abc import ABC, abstractmethod

class RecordProcessor(ABC):
    @abstractmethod
    def __init__(self, app: flask.Flask):
        pass

    @abstractmethod
    def process(self, destionation, id, data) -> None:
        pass

class KafkaProcessor(RecordProcessor):
    def __init__(self, app: flask.Flask):
        kafka_conf = {
            'bootstrap.servers': app.config['KAFKA_BOOTSTRAP_SERVERS'],
            'client.id': socket.gethostname()
        }
        self.producer = Producer(kafka_conf)

    def process(self, destination, id, data: Dict[str, Any]) -> None:
        self.producer.produce(destination, 
                              key=json.dumps({ 'owner_id': id }).encode(), 
                              value=json.dumps(data).encode())
        

class ConsoleProcessor(RecordProcessor):
    def __init__(self, app: flask.Flask):
        self.logger = app.logger

    def process(self, destination, id, data: Dict[str, Any]) -> None:
        self.logger.info("""
                         Destination: %s
                         Id: %s
                         data: %s
                         """, destination, id, json.dumps(data, indent=4))
        