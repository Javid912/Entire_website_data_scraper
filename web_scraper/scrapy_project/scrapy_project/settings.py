BOT_NAME = 'scrapy_project'

SPIDER_MODULES = ['scrapy_project.spiders']
NEWSPIDER_MODULE = 'scrapy_project.spiders'

ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 2  # 1-3 seconds, can randomize in spider
CONCURRENT_REQUESTS = 12  # 8-16
AUTOTHROTTLE_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (compatible; WebScraperBot/1.0; +https://kijufi.de)'
COOKIES_ENABLED = True

ITEM_PIPELINES = {
    'scrapy_project.pipelines.CleanDataPipeline': 300,
    'scrapy_project.pipelines.DuplicatesPipeline': 400,
    'scrapy_project.pipelines.JsonExportPipeline': 500,
}

LOG_LEVEL = 'INFO'

# Playwright integration
DOWNLOAD_HANDLERS = {
    'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
    'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
}
PLAYWRIGHT_BROWSER_TYPE = 'chromium'
PLAYWRIGHT_LAUNCH_OPTIONS = {'headless': True} 