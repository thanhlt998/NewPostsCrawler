PERSIST_QUEUE_PATH = 'urls-queue'
NEW_URLS_TOPIC = "new-urls"
NO_CONCURRENT_URLS = 100

SETTINGS = {
    'LOG_FILE': 'log/url_crawler.log',

    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'random_useragent.RandomUserAgentMiddleware': 10,
    },

    'ITEM_PIPELINES': {
        'pipelines.KafkaItemPipeline': 300
    },

    # 'DUPEFILTER_CLASS': 'filters.BLOOMDupeFilter',
    'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',

    'DEPTH_PRIORITY': 1,
    # 'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'LOG_LEVEL': 'INFO',
    'COOKIES_ENABLED': False,
    'TELNETCONSOLE_PORT': None,

    'USER_AGENT_LIST': 'data/user_agent.txt',

    # Kafka settings
    # 'BOOTSTRAP_SERVERS': ['localhost:9092'],
    'BOOTSTRAP_SERVERS': ['192.168.1.239:9092'],
    'TOPIC': 'adfilex-url-crawl'
}