from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
import logging
from logging.handlers import RotatingFileHandler
from twisted.internet import reactor
from twisted.internet.task import deferLater
import sys
import time
import os

from connection import MysqlConnection
from redis_server import RedisServer
from crawler import NewPostCrawler
from settings.domain_crawler_settings import MYSQL_DB, REDIS_SERVER, NO_MAX_CONCURRENT_SPIDER, SETTINGS


def crawl():
    redis_server.set_no_domains(len(domain_ids))
    i = 0
    while i < min(NO_MAX_CONCURRENT_SPIDER, len(domain_ids)):
        crawl_new_domain()
        i += 1


def crawl_new_domain(result=None):
    connection_ = MysqlConnection(host=MYSQL_DB['host'], user=MYSQL_DB['user'], password=MYSQL_DB['password'],
                                 db=MYSQL_DB['db'])
    domain_id = redis_server.get_domains_to_crawl('domain_ids')
    domain = connection_.get_domain_object_by_domain_id(domain_id=int(domain_id))
    connection_.close_connection()
    deffered = process.crawl(NewPostCrawler, name="new_posts_crawler", domain=domain)
    deffered.addCallback(sleep, None, seconds=10)
    deffered.addCallback(crawl_new_domain)


def sleep(self, *args, seconds):
    """Non blocking sleep callback"""
    return deferLater(reactor, seconds, lambda: None)


if __name__ == '__main__':
    connection = MysqlConnection(host=MYSQL_DB['host'], user=MYSQL_DB['user'], password=MYSQL_DB['password'],
                                 db=MYSQL_DB['db'])
    redis_server = RedisServer(host=REDIS_SERVER['host'], port=REDIS_SERVER['port'], db=REDIS_SERVER['db'])

    domain_ids = connection.get_domain_id_list()
    connection.close_connection()
    redis_server.set_list("domain_ids", domain_ids)

    # settings
    s = get_project_settings()
    s.update(SETTINGS)

    # crawler process
    process = CrawlerProcess(s)

    # logging
    configure_logging(install_root_handler=False)

    root_logger = logging.getLogger()
    log_formatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rotating_file_log = RotatingFileHandler('log/error_log.log', maxBytes=10485760, backupCount=1)
    rotating_file_log.setLevel(logging.ERROR)
    rotating_file_log.setFormatter(log_formatter)
    root_logger.addHandler(rotating_file_log)

    # start crawling
    crawl()
    process.start()

    time.sleep(0.5)
    os.execl(sys.executable, sys.executable, *sys.argv)
