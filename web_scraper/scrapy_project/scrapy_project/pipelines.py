import json
import os
from scrapy.exceptions import DropItem

class CleanDataPipeline:
    def process_item(self, item, spider):
        # Implement data cleaning here
        return item

class DuplicatesPipeline:
    def __init__(self):
        self.seen_urls = set()

    def process_item(self, item, spider):
        if item['url'] in self.seen_urls:
            raise DropItem(f"Duplicate item found: {item['url']}")
        self.seen_urls.add(item['url'])
        return item

class JsonExportPipeline:
    def open_spider(self, spider):
        output_dir = os.path.join(os.path.dirname(__file__), '../../data/scraped_data')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'kijufi_data.json')
        self.file = open(output_path, 'w', encoding='utf-8')
        self.first = True
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        if not self.first:
            self.file.write(',\n')
        self.first = False
        line = json.dumps(dict(item), ensure_ascii=False)
        self.file.write(line)
        return item 