import scrapy
from typing import List

class ScrapedItem(scrapy.Item):
    url = scrapy.Field()  # The URL of the scraped page
    title = scrapy.Field()  # The title of the page
    content = scrapy.Field()  # Main text content extracted from the page
    meta_description = scrapy.Field()  # Meta description if available
    scraped_at = scrapy.Field()  # Timestamp of when the page was scraped
    links = scrapy.Field()  # List of links found on the page
    images = scrapy.Field()  # List of image URLs found on the page
    page_type = scrapy.Field()  # Type/category of the page (optional)
    emails = scrapy.Field()  # List of emails found in the content 