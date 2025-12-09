import os
import pymongo
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter

# 1. Pipeline: Filtering and Limit Control
class FilterAndLimitPipeline:
    """
    Pipeline to filter movies based on their rating and limit the total number of scraped items.
    Allows only items with rating >= 8.0 and stops processing after 1000 items.
    """
    
    def __init__(self, limit: int = 1000, min_rating: float = 8.0):
        self.limit = limit
        self.min_rating = min_rating
        self.count = 0
    
    @classmethod
    def from_crawler(cls, crawler):
        # We can retrieve values from Settings or use the defaults defined above
        return cls()

    def process_item(self, item, spider):
        # Rating Check: Ensure the movie has a rating and it meets the minimum requirement
        if not item.get("rating") or item["rating"] < self.min_rating:
            raise DropItem(f"Rating too low: {item.get('rating')}")

        # Limit Check: Ensure we do not exceed the target count
        if self.count >= self.limit:
            # Drop the item if limit is reached to stop further processing for this item
            raise DropItem("Limit reached")
        
        self.count += 1
        return item

# 2. Pipeline: MongoDB Storage
class MongoPipeline:
    """
    Pipeline to store scraped items into a MongoDB database.
    Uses an 'upsert' strategy to avoid duplicate entries based on the movie URL.
    """
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        # Fetch database connection details from the project settings
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI", "mongodb://localhost:27017"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "imdb_db"),
            collection_name=crawler.settings.get("MONGO_COLLECTION", "top_movies")
        )

    def open_spider(self, spider):
        # Initialize the MongoDB client and database connection when the spider opens
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
        # Create a unique index on the 'url' field to prevent duplicate records
        self.db[self.collection_name].create_index("url", unique=True)

    def close_spider(self, spider):
        # Close the connection when the spider finishes
        self.client.close()

    def process_item(self, item, spider):
        # Convert the Scrapy Item to a standard Python dictionary
        data = ItemAdapter(item).asdict()
        
        # Upsert Operation: Update the record if it exists (based on URL), otherwise insert it.
        self.db[self.collection_name].update_one(
            {"url": data["url"]},
            {"$set": data},
            upsert=True
        )
        spider.logger.debug(f"Upserted to MongoDB: {data.get('title')}")
        return item