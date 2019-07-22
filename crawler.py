from scrapy import Spider, Request

from utils import get_url_with_scheme, is_resource_url, fix_url
from items import UrlItem
from connection import MysqlConnection
from settings import MYSQL_DB
from proto_message import UrlHTML


class NewPostCrawler(Spider):
    # name = 'new_post_crawler'

    def __init__(self, name=None, **kwargs):
        self.domain = kwargs.get('domain')
        self.allowed_domains = [self.domain.domain_name]
        super(NewPostCrawler, self).__init__(name, **kwargs)

    def start_requests(self):
        yield Request(url=get_url_with_scheme(self.domain.domain_name), callback=self.parse,
                      errback=self.domain_error_back)

    def parse(self, response):
        urls = [fix_url(response.urljoin(url.strip())) for url in response.xpath("//a/@href").getall() if
                not is_resource_url(url)]

        for url in urls:
            if not self.domain.is_crawled_url(url):
                # print(url)
                yield Request(url=url, callback=self.get_html, errback=self.page_error_back)

    def domain_error_back(self, failure):
        self.logger.error(f'Domain error: {repr(failure)}')

    def get_html(self, response):
        self.domain.add_new_url(response.request.url)
        yield UrlItem(url=response.request.url, raw=response.text)

    def page_error_back(self, failure):
        self.logger.error(f'Page error: {repr(failure)}, url: {failure.request.url}')

    def close(self, spider, reason):
        connection = MysqlConnection(host=MYSQL_DB['host'], user=MYSQL_DB['user'], password=MYSQL_DB['password'],
                                     db=MYSQL_DB['db'])
        connection.update_domain_object(self.domain)
        connection.close_connection()
