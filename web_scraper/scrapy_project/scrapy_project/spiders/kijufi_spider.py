import scrapy
from scrapy.http import Request
from ..items import KijufiItem
from datetime import datetime
from urllib.parse import urljoin, urlparse
import random
import re
from readability import Document
from bs4 import BeautifulSoup

class KijufiSpider(scrapy.Spider):
    name = 'kijufi_spider'
    allowed_domains = ['kijufi.de']
    start_urls = ['https://kijufi.de/']

    custom_settings = {
        'PLAYWRIGHT_PAGE_METHODS': [
            {"method": "wait_for_timeout", "args": [1000]}
        ]
    }

    def parse(self, response):
        item = KijufiItem()
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

        # Follow internal links
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
        parsed = urlparse(url)
        return parsed.netloc.endswith('kijufi.de')

    def errback(self, failure):
        self.logger.error(f"Request failed: {failure.request.url} - {failure.value}") 