import os
import json
import socket
import ssl

from kafka import KafkaConsumer, KafkaProducer

_kafka_client_id = f'edge-vm-{socket.gethostname()}'

ssl_context = ssl.create_default_context(
    cafile="/usr/local/share/ca-certificates/rootCA.crt"
)
ssl_context.check_hostname = False


class KafkaSingleton:

    def init_kafka_bootstrap_server(self, bootstrap_server: str, user: str, password: str):
        if bootstrap_server.strip() == '':
            raise ValueError('Bootstrap server cannot be empty')
        self._bootstrap_server = bootstrap_server
        self._user = user
        self._password = password

    def init_kafka_pubsub(self, results_topic: str):
        self.producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_server,
            client_id=_kafka_client_id,

            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=self._user,
            sasl_plain_password=self._password,
            ssl_context=ssl_context,

            value_serializer=lambda m: json.dumps(m).encode(),
            key_serializer=lambda m: json.dumps(m).encode()
        )

        # auto_offset_reset is set to earliest because the task result consumer
        # always reads from the beginning. Besides, it should not commit the message
        # offset for the same reason
        self.results_consumer = KafkaConsumer(
            bootstrap_servers=self._bootstrap_server,
            client_id=_kafka_client_id,

            security_protocol="SASL_SSL",
            sasl_mechanism="PLAIN",
            sasl_plain_username=self._user,
            sasl_plain_password=self._password,
            ssl_context=ssl_context,

            value_deserializer=lambda m: json.loads(m.decode()),
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        self.results_consumer.subscribe(topics=[results_topic])
        # tps = [TopicPartition(topic, p) 
        #        for p in self.results_consumer.partitions_for_topic(results_topic)]
        # self.results_consumer.assign(tps)

kafka = KafkaSingleton()