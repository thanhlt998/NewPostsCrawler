from bloom_filter import BloomFilter


class Domain:
    def __init__(self, domain_name, **kwargs):
        self.domain_name = domain_name
        self.domain_id = kwargs.get('domain_id')
        self.crawled_urls = kwargs.get('crawled_urls') if kwargs.get('crawled_urls') else []
        self.new_urls = set()
        self.filter = BloomFilter(max_elements=100000, error_rate=0.00001)

    def is_crawled_url(self, url):
        return url in self.filter

    def add_new_url(self, url):
        self.new_urls.add(url)
