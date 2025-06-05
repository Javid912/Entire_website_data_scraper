import scrapy
from typing import List

class KijufiItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    meta_description = scrapy.Field()
    scraped_at = scrapy.Field()
    links = scrapy.Field()
    images = scrapy.Field()
    page_type = scrapy.Field()
    emails = scrapy.Field() 