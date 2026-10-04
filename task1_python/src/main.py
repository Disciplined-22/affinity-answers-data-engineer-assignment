import asyncio
import json
import logging
import os
import sys
from dotenv import load_dotenv

# Configure logging format and output standard
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Ensure local imports resolve accurately
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import MongoStorage
from scraper import MDComputersScraper


async def main():
    # Load configuration from environment file
    load_dotenv()

    # Capture input query from command line arguments or interactive input
    if len(sys.argv) > 1:
        search_term = " ".join(sys.argv[1:])
    else:
        search_term = input("Enter product search term (e.g., 'external harddrive'): ").strip()

    if not search_term:
        logger.error("Search term cannot be empty.")
        return

    logger.info("Starting Scraping Workflow for: '%s'", search_term)

    # Step 1 & 2: Launch Playwright, retrieve DOM, and parse product data
    headless_setting =  False
    scraper = MDComputersScraper(headless=headless_setting)
    
    products = await scraper.fetch_search_results(search_term)

    logger.info("Extraction Summary: Found %d products matching '%s'.", len(products), search_term)


    
if __name__ == "__main__":
    # Execute Option B: Async Playwright via asyncio.run()
    asyncio.run(main())