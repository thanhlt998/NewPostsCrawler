# SETTINGS
## New posts crawler
Change settings in settings/domain_crawler_settings.py
```
NO_MAX_CONCURRENT_SPIDER: number of concurrent domains to crawl
EXPIRE_WINDOWS_TIME_SIZE: time expire to crawl a duplicated url again
MYSQL_DB: host, user, password, db - connect to MySQL server
REDIS_SERVER: host, port, db - connect to Redis

SETTINGS: settings of scrapy
    ...
    USER_AGENT_LIST: file contains user agent list
    BOOTSTRAP_SERVERS: Kafka server address
    TOPIC: topic on Kafka server to push raw html into
```

## Urls crawler
```
PERSIST_QUEUE_PATH: path to save data in persist queue on disk
NEW_URLS_TOPIC: topic on kafka to push url from api into
SETTINGS: settings of scrapy
    ...
    USER_AGENT_LIST: file contains user agent list
    BOOTSTRAP_SERVERS: Kafka server address
    TOPIC: topic on Kafka server to push raw html into
```

### API settings
```
BIND_ADDRESS: address to bind the api
BIND_PORT: port to bind the api
REDIS_SERVER: host, port, db - connect to Redis
MYSQL_DB: host, user, password, db - connect to MySQL server
```

## API urls
```
1. Add urls to Url crawler
    - Url: http://address:port/add_urls
    - Method: POST
    - Content-Type: application/json
    - Data json: {"urls" : []}
    
2. Add domains into loop domains to crawl new posts 
    - Url: http://address:port/add_domains
    - Method: POST
    - Content-Type: application/json
    - Data json: {"domains" : []}

3. Remove domains from loop domains
    - Url: http://address:port/remove_domains
    - Method: POST
    - Content-Type: application/json
    - Data json: {"domains" : []}
```
# Run
Using python 3, install requirements before running
```
pip install -r requirements.txt
```
## Run new posts crawler:
```
python main.py
```
## Run urls crawler to crawl url received from api
```
python run_url_crawler.py
```
## Run api
```
python run_api.py
```