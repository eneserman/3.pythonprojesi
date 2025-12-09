import scrapy
from imdb_scraper.items import Movie
import logging
from typing import Iterator

# Set up logger for tracking progress
logger = logging.getLogger(__name__)

class ImdbTopSpider(scrapy.Spider):
    """
    Spider to scrape top-rated AND popular movies from IMDb.
    """
    name = "imdb_top"
    allowed_domains = ["imdb.com"]
    
    LIMIT = 1000
    MIN_RATING = 8.0
    # NEW: Minimum vote threshold (To filter out niche/obscure movies)
    MIN_VOTES = 25000 
    collected_count = 0

    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "ROBOTSTXT_OBEY": False,
        "LOG_LEVEL": "INFO",
        "COOKIES_ENABLED": False,
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 0.25 
    }

    def start_requests(self):
        """
        Performs a year-based crawl.
        FILTER UPDATE: 
        - Rating: Between 8.0 - 10.0
        - Vote Count: At least 25,000 (num_votes=25000,)
        - Sort: By rating (sort=user_rating,desc)
        """
        start_year = 2024
        years_to_scrape = 55 
        
        for i in range(years_to_scrape):
            year = start_year - i
            
            # URL PARAMETERS:
            # title_type=feature      -> Feature films only
            # release_date=...        -> Released in that year
            # user_rating=8.0,10.0    -> Rating range
            # num_votes=25000,        -> CRITICAL POINT: Must have at least 25,000 votes (Comma implies "min")
            # sort=user_rating,desc   -> Sort from highest rating downwards
            # count=50                -> Take the top 50 movies from each year
            
            url = (f"https://www.imdb.com/search/title/?"
                   f"title_type=feature&"
                   f"release_date={year}-01-01,{year}-12-31&"
                   f"user_rating=8.0,10.0&"
                   f"num_votes={self.MIN_VOTES},&" 
                   f"sort=user_rating,desc&"
                   f"count=50")
                   
            logger.info(f"🚀 Queuing request for YEAR: {year} (Min Votes: {self.MIN_VOTES})")
            yield scrapy.Request(url=url, callback=self.parse_list)

    def parse_list(self, response: scrapy.http.Response):
        movies = response.css("li.ipc-metadata-list-summary-item")
        
        if not movies:
            return

        for movie_container in movies:
            if self.collected_count >= self.LIMIT:
                break 

            # --- Title ---
            title_raw = movie_container.css("h3.ipc-title__text::text").get()
            title = title_raw.split(". ", 1)[1].strip() if title_raw and ". " in title_raw else (title_raw or "Unknown")

            # --- URL ---
            relative_url = movie_container.css("a.ipc-title-link-wrapper::attr(href)").get()
            full_url = response.urljoin(relative_url.split("?")[0]) if relative_url else ""
            
            # --- Year ---
            year = movie_container.css(".dli-title-metadata-item::text").get()
            
            # --- Rating ---
            rating_text = movie_container.css(".ipc-rating-star--rating::text").get()
            rating = float(rating_text) if rating_text else 0.0
            
            if rating < self.MIN_RATING:
                continue

            # --- Create Item ---
            movie_item = Movie(
                title=title, 
                year=year, 
                rating=rating, 
                director="Loading...", 
                url=full_url
            )
            
            if full_url:
                yield scrapy.Request(
                    url=full_url, 
                    callback=self.parse_detail, 
                    meta={'movie_item': movie_item}
                )

    def parse_detail(self, response):
        movie_item = response.meta['movie_item']
        
        # --- Extract Director ---
        director = response.xpath("//li[contains(@class, 'ipc-metadata-list__item') and .//span[contains(text(), 'Director')]]//a/text()").get()
        
        if not director:
             director = response.css("a.ipc-metadata-list-item__list-content-item--link::text").get()

        movie_item['director'] = director if director else "Unknown"
        
        self.collected_count += 1
        
        if self.collected_count <= self.LIMIT + 50:
             yield movie_item