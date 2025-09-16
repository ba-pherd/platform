import json
import socket
from kafka import KafkaConsumer, KafkaProducer


class KafkaSingleton:
    _instance = None
    
    _consumer_topic: str = None

    
    def _validate_server(self):
        if self._bootstrap_server == None:
            raise ValueError('init_server has not been called')


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KafkaSingleton, cls).__new__(cls)
        return cls._instance
    

    def init_server(self, bootstrap_server: str):
        if bootstrap_server.strip() == '':
            raise ValueError('Bootstrap server cannot be empty')
        self._bootstrap_server = bootstrap_server
        self._client_id = f'edge-vm-{socket.gethostname()}'

        self.kafka_producer = KafkaProducer(
            bootstrap_servers=self._bootstrap_server,
            client_id=self._client_id,
            value_serializer=lambda m: json.dumps(m).encode(),
            key_serializer=lambda m: json.dumps(m).encode()
        )

    
    def init_consumer(self, topic: str):
        self._validate_server()

        # auto_offset_reset is set to earliest because the task result consumer
        # always reads from the beginning. Besides, it should not commit the message
        # offset for the same reason
        self.kafka_results_consumer = KafkaConsumer(
            bootstrap_servers=self._bootstrap_server,
            client_id=self._client_id,
            value_deserializer=lambda m: json.loads(m.decode()),
            auto_offset_reset='earliest',
            enable_auto_commit=False
        )
        self.kafka_results_consumer.subscribe(topics=[topic])
        # tps = [TopicPartition(topic, p) 
        #        for p in self.kafka_results_consumer.partitions_for_topic(topic)]
        # self.kafka_results_consumer.assign(tps)
        
