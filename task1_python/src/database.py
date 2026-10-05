import os
from typing import Dict, List, Optional
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging


# Initialize a module-level logger specifically for database operations.
# This avoids importing 'logger' from main.py and prevents circular dependencies.
logger = logging.getLogger(__name__)

class MongoStorage:
    """Manages connection and persistence operations for MongoDB."""

    def __init__(self):
        """
        Initialize the MongoDB client using environment variables or a direct URI.
        Falls back gracefully if connection fails.
        """
        # 1. Look for environment variable named MONGO_URI
        self.mongo_uri = os.getenv("MONGO_URI")
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection = None
        
        self._connect()

    def _connect(self) -> None:
        """Establish MongoDB connection and verify cluster health."""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=3000)
            self.db = self.client["md_computers_7xK4p9Q2"]
            self.collection = self.db["products_7xK4p9Q2"]
            
            # Test connection readiness
            self.client.server_info()
        except PyMongoError as e:
            logger.info(f"[Database Warning] MongoDB connection failed ({e}). Proceeding without database storage...")
            self.client = None

    def save_products(self, products: List[Dict]) -> int:
        """
        Saves extracted product dictionaries into the MongoDB collection.
        
        Args:
            products: List of product data dictionaries.
            
        Returns:
            int: Number of records inserted.
        """
        if not self.client or not products:
            return 0

        try:
            result = self.collection.insert_many(products) # inserts has [{object_id}, {object_id}, {object_id} ]
            inserted_count = len(result.inserted_ids)
            logger.info(f"[Database] Successfully saved {inserted_count} products.")
            return inserted_count
        except PyMongoError as e:
            logger.info(f"[Database Error] Failed to write documents to MongoDB: {e}")
            return 0

    def close(self) -> None:
        """Close the MongoDB client connection."""
        if self.client:
            self.client.close()
            logger.info("[Database] MongoDB connection closed.")