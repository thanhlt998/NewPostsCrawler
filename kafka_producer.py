from kafka import KafkaProducer


class Producer:
    def __init__(self, bootstrap_servers):
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers, api_version=(0, 10))

    def send_message(self, topic, value=None, key=None, headers=None, partition=None, timestamp_ms=None):
        self.producer.send(topic, value=value, key=key, headers=headers, partition=partition, timestamp_ms=timestamp_ms)

    def close(self):
        self.producer.close()
