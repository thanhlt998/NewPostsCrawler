from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess

from crawler import UrlsCrawler
from settings.url_crawler_settings import SETTINGS


def crawl_urls():
    pass


if __name__ == '__main__':
    # settings
    s = get_project_settings()
    s.update(SETTINGS)

    # crawler process
    process = CrawlerProcess(s)

    # logging
    configure_logging()

    process.crawl(UrlsCrawler, name='url_crawler')
    process.start()
