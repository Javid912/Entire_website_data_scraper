import subprocess
import sys

def run_spider(spider_name: str = 'main_spider'):
    cmd = [sys.executable, '-m', 'scrapy', 'crawl', spider_name]
    subprocess.run(cmd)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run a Scrapy spider')
    parser.add_argument('--spider', type=str, default='main_spider', help='Spider name to run')
    args = parser.parse_args()
    run_spider(args.spider) 