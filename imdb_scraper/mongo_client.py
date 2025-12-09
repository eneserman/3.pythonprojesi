"""
Simple MongoDB client for inserting movie records.
Used by MoviePipeline. Keeps project modular and testable.
"""

from pymongo import MongoClient


class MongoDBClient:
    """Handles MongoDB database operations."""

    def __init__(self, uri="mongodb://localhost:27017/", db_name="imdb_project", collection_name="top_movies"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_movies(self, movies):
        """Insert multiple movie dictionaries into MongoDB."""
        if movies:
            self.collection.insert_many(movies)

    def close(self):
        """Close database connection."""
        self.client.close()
