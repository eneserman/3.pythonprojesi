# imdb_scraper/items.py

import scrapy
from dataclasses import dataclass

class Movie(scrapy.Item):
    """Scrapy Item definition for IMDb movie data."""
    
    # Define the fields for your scraped data
    title = scrapy.Field()
    year = scrapy.Field()
    rating = scrapy.Field()
    director = scrapy.Field()
    url = scrapy.Field()
    # Add other fields you might scrape (e.g., votes, runtime)