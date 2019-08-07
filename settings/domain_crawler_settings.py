NO_MAX_CONCURRENT_SPIDER = 64
EXPIRE_WINDOWS_TIME_SIZE = 2

MYSQL_DB = {
    'host': '192.168.1.239',
    'user': 'thanhlt',
    'password': 'ThanhLT@MySQL2019',
    'db': 'TTS'
}
# MYSQL_DB = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': '123456',
#     'db': 'domain_rank'
# }

REDIS_SERVER = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}

SETTINGS = {
    'DEPTH_LIMIT': 1,
    'LOG_FILE': 'log/file.log',

    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
        'random_useragent.RandomUserAgentMiddleware': 10,
    },

    'ITEM_PIPELINES': {
        'pipelines.KafkaItemPipeline': 300
    },

    # 'DUPEFILTER_CLASS': 'filters.BLOOMDupeFilter',

    'DEPTH_PRIORITY': 1,
    'DOWNLOAD_DELAY': 1,
    'CONCURRENT_REQUESTS': 1,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
    'LOG_LEVEL': 'INFO',
    'COOKIES_ENABLED': False,
    'TELNETCONSOLE_PORT': None,
    'REDIRECT_ENABLED': False,

    'USER_AGENT_LIST': 'data/user_agent.txt',

    # 'CLOSESPIDER_TIMEOUT': 3600,  # 1 hours

    # Kafka settings
    # 'BOOTSTRAP_SERVERS': ['localhost:9092'],
    'BOOTSTRAP_SERVERS': ['192.168.1.239:9092'],
    'TOPIC': 'adfilex-url-crawl'
}
