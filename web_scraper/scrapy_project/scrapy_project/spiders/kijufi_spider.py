import scrapy
from scrapy.http import Request
from ..items import ScrapedItem
from datetime import datetime
from urllib.parse import urljoin, urlparse
import random
import re
from readability import Document
from bs4 import BeautifulSoup

class MainSpider(scrapy.Spider):
    name = 'main_spider'
    allowed_domains = []  # Allow all domains by default
    start_urls = []  # Will be set dynamically if needed

    custom_settings = {
        'PLAYWRIGHT_PAGE_METHODS': [
            {"method": "wait_for_timeout", "args": [1000]}
        ]
    }

    def start_requests(self):
        # Allow passing start_urls via spider arguments
        url = getattr(self, 'start_url', None)
        if url:
            # Start from the user-provided URL
            yield scrapy.Request(url, callback=self.parse, meta={'playwright': True})
        else:
            # Start from default start_urls if provided
            for url in self.start_urls:
                yield scrapy.Request(url, callback=self.parse, meta={'playwright': True})

    def parse(self, response):
        item = ScrapedItem()
        item['url'] = response.url
        item['title'] = response.xpath('//title/text()').get()
        # Use readability-lxml to extract main content
        doc = Document(response.text)
        main_html = doc.summary()  # HTML of main content
        # Use BeautifulSoup to get clean text
        soup = BeautifulSoup(main_html, "lxml")
        text_content = soup.get_text(separator=' ', strip=True)
        item['content'] = text_content
        # Extract emails from content
        item['emails'] = re.findall(r'[\w\.-]+@[\w\.-]+', text_content)
        # Extract links (keep only unique, meaningful links)
        links = [urljoin(response.url, href) for href in response.xpath('//a/@href').getall()]
        item['links'] = list(set([l for l in links if self.is_internal(l) or l.startswith('http')]))
        yield item

        # Follow internal links (for full site crawl)
        for link in item['links']:
            if self.is_internal(link):
                yield Request(
                    link,
                    callback=self.parse,
                    errback=self.errback,
                    meta={
                        'playwright': True,
                        'playwright_page_methods': [
                            {"method": "wait_for_timeout", "args": [random.randint(1000, 3000)]}
                        ]
                    },
                    headers={
                        'User-Agent': self.settings.get('USER_AGENT')
                    }
                )

    def is_internal(self, url):
        # Consider all links as internal for generic use, or customize as needed
        parsed = urlparse(url)
        return True

    def errback(self, failure):
        # Log failed requests
        self.logger.error(f"Request failed: {failure.request.url} - {failure.value}") 