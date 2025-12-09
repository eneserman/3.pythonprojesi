import unittest
import os
import sys
from unittest.mock import MagicMock

# Add project root for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from imdb_scraper.pipelines import MoviePipeline
from imdb_scraper.mongo_client import MongoDBClient


class TestMoviePipeline(unittest.TestCase):
    """Unit tests for movie pipeline filtering and DB interaction."""

    def setUp(self):
        self.mock_scraper = MagicMock()
        self.mock_db = MagicMock(spec=MongoDBClient)
        self.pipeline = MoviePipeline(scraper=self.mock_scraper, database=self.mock_db)

    def test_filter_movies_by_rating(self):
        sample = [
            {"title": "A", "rating": 8.5},
            {"title": "B", "rating": 7.2},
            {"title": "C", "rating": 8.1},
        ]

        filtered = self.pipeline.filter_movies(sample)

        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(m["rating"] >= 8.0 for m in filtered))

    def test_database_insert_called(self):
        sample = [
            {"title": "Interstellar", "rating": 8.6},
            {"title": "Inception", "rating": 8.8},
        ]

        self.pipeline.database.insert_movies(sample)
        self.pipeline.database.insert_movies.assert_called_once_with(sample)


if __name__ == "__main__":
    unittest.main()
