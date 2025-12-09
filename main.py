from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl("imdb_top")  # spider name burası!
    process.start()

if __name__ == "__main__":
    run_spider()
