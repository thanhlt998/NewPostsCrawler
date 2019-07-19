from kafka_producer import Producer

from items import UrlItem
from proto_message import UrlHTML


class KafkaItemPipeline:
    def __init__(self, bootstrap_servers, topic):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            bootstrap_servers=crawler.settings.get('BOOTSTRAP_SERVERS'),
            topic=crawler.settings.get('TOPIC')
        )

    def open_spider(self, spider):
        self.producer = Producer(self.bootstrap_servers)

    def close_spider(self, spider):
        if self.producer:
            self.producer.close()

    def process_item(self, item, spider):
        if isinstance(item, UrlItem):
            self.producer.send_message(self.topic, UrlHTML.serialize(UrlHTML(url=item['url'], raw=item['raw'])))
