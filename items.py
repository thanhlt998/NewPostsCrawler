from scrapy import Item, Field


class UrlItem(Item):
    url = Field()
    raw = Field()
