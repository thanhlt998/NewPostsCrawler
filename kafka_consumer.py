import snappy
import persistqueue
from kafka import KafkaConsumer

from proto_message import UrlsMessage
from settings.url_crawler_settings import PERSIST_QUEUE_PATH, NEW_URLS_TOPIC


if __name__ == '__main__':
    consumer = KafkaConsumer(NEW_URLS_TOPIC, bootstrap_servers=['localhost:9092'])
    q = persistqueue.SQLiteQueue(PERSIST_QUEUE_PATH, auto_commit=True)
    for message in consumer:
        data = UrlsMessage.deserialize(snappy.decompress(message.value))
        for url in data.urls:
            q.put(url)
