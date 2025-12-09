BOT_NAME = "imdb_scraper"

SPIDER_MODULES = ["imdb_scraper.spiders"]
NEWSPIDER_MODULE = "imdb_scraper.spiders"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
    "imdb_scraper.pipelines.FilterAndLimitPipeline": 300,
    "imdb_scraper.pipelines.MongoPipeline": 400,
}
